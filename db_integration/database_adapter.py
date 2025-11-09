"""Database adapter that supports both Docker PostgreSQL and Supabase."""

import os
from typing import Optional
from supabase import create_client, Client
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()


class DatabaseAdapter:
    """Adapter that works with both Docker PostgreSQL and Supabase."""
    
    def __init__(self):
        """Initialize database connection."""
        self.use_supabase = os.getenv('USE_SUPABASE', 'false').lower() == 'true'
        self.supabase_client: Optional[Client] = None
        self.postgres_conn = None
        
        if self.use_supabase:
            # Use Supabase client
            supabase_url = os.getenv('SUPABASE_URL')
            supabase_key = os.getenv('SUPABASE_KEY')
            
            if not supabase_url or not supabase_key:
                raise ValueError(
                    "USE_SUPABASE=true but SUPABASE_URL and SUPABASE_KEY must be set"
                )
            
            self.supabase_client = create_client(supabase_url, supabase_key)
        else:
            # Use direct PostgreSQL connection
            db_host = os.getenv('DB_HOST', 'database')
            db_port = os.getenv('DB_PORT', '5432')
            db_name = os.getenv('DB_NAME', os.getenv('POSTGRES_DB', 'evolveiq_db'))
            db_user = os.getenv('DB_USER', os.getenv('POSTGRES_USER', 'evolveiq'))
            db_password = os.getenv('DB_PASSWORD', os.getenv('POSTGRES_PASSWORD', 'evolveiq_password'))
            
            try:
                self.postgres_conn = psycopg2.connect(
                    host=db_host,
                    port=db_port,
                    database=db_name,
                    user=db_user,
                    password=db_password
                )
            except Exception as e:
                raise ValueError(f"Failed to connect to PostgreSQL: {str(e)}")
    
    def table(self, table_name: str):
        """Get table interface compatible with Supabase client."""
        if self.use_supabase:
            return self.supabase_client.table(table_name)
        else:
            return PostgresTableAdapter(self.postgres_conn, table_name)
    
    def rpc(self, function_name: str, params: dict = None):
        """Call a PostgreSQL function (RPC) - compatible with Supabase client."""
        if self.use_supabase:
            return self.supabase_client.rpc(function_name, params)
        else:
            return PostgresRPCBuilder(self.postgres_conn, function_name, params or {})
    
    def close(self):
        """Close database connection."""
        if self.postgres_conn:
            self.postgres_conn.close()


class PostgresTableAdapter:
    """Adapter to make PostgreSQL queries compatible with Supabase client interface."""
    
    def __init__(self, conn, table_name: str):
        self.conn = conn
        self.table_name = table_name
    
    def select(self, columns: str = '*'):
        """Start a SELECT query."""
        return PostgresQueryBuilder(self.conn, self.table_name, 'select', columns)
    
    def insert(self, data: dict):
        """Insert data - returns query builder for chaining."""
        return PostgresInsertBuilder(self.conn, self.table_name, data, 'insert')
    
    def upsert(self, data: dict, on_conflict: Optional[str] = None):
        """Upsert data - returns query builder for chaining."""
        return PostgresInsertBuilder(self.conn, self.table_name, data, 'upsert', on_conflict)
    
    def delete(self):
        """Start a DELETE query."""
        return PostgresQueryBuilder(self.conn, self.table_name, 'delete')
    
    def update(self, data: dict):
        """Start an UPDATE query."""
        return PostgresQueryBuilder(self.conn, self.table_name, 'update', update_data=data)


class PostgresQueryBuilder:
    """Query builder for PostgreSQL that mimics Supabase client interface."""
    
    def __init__(self, conn, table_name: str, operation: str, columns: str = '*', update_data: Optional[dict] = None):
        self.conn = conn
        self.table_name = table_name
        self.operation = operation
        self.columns = columns
        self.update_data = update_data
        self.filters = []
        self.limit_val = None
        self.order_by = None
    
    def eq(self, column: str, value):
        """Add equality filter."""
        self.filters.append((column, '=', value))
        return self
    
    def neq(self, column: str, value):
        """Add not-equal filter."""
        self.filters.append((column, '!=', value))
        return self
    
    def limit(self, count: int):
        """Set limit."""
        self.limit_val = count
        return self
    
    def order(self, column: str, desc: bool = False):
        """Set order by."""
        self.order_by = (column, desc)
        return self
    
    def execute(self):
        """Execute the query."""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        if self.operation == 'select':
            query = f"SELECT {self.columns} FROM {self.table_name}"
            where_clause = self._build_where()
            if where_clause:
                query += f" WHERE {where_clause}"
            if self.order_by:
                query += f" ORDER BY {self.order_by[0]} {'DESC' if self.order_by[1] else 'ASC'}"
            if self.limit_val:
                query += f" LIMIT {self.limit_val}"
            
            cursor.execute(query, [f[2] for f in self.filters])
            results = cursor.fetchall()
            cursor.close()
            return PostgresResult(results)
        
        elif self.operation == 'delete':
            query = f"DELETE FROM {self.table_name}"
            where_clause = self._build_where()
            if where_clause:
                query += f" WHERE {where_clause}"
            cursor.execute(query, [f[2] for f in self.filters])
            self.conn.commit()
            cursor.close()
            return PostgresResult([])
        
        elif self.operation == 'update':
            if not self.update_data:
                raise ValueError("Update data required for update operation")
            set_clause = ', '.join([f"{k} = %s" for k in self.update_data.keys()])
            query = f"UPDATE {self.table_name} SET {set_clause}"
            where_clause = self._build_where()
            if where_clause:
                query += f" WHERE {where_clause}"
            query += " RETURNING *"
            values = list(self.update_data.values()) + [f[2] for f in self.filters]
            cursor.execute(query, values)
            self.conn.commit()
            results = cursor.fetchall()
            cursor.close()
            return PostgresResult(results)
    
    def _build_where(self) -> str:
        """Build WHERE clause from filters."""
        if not self.filters:
            return ""
        conditions = []
        for i, (col, op, val) in enumerate(self.filters):
            conditions.append(f"{col} {op} %s")
        return " AND ".join(conditions)


class PostgresInsertBuilder:
    """Builder for insert/upsert operations that mimics Supabase chaining."""
    
    def __init__(self, conn, table_name: str, data: dict, operation: str, on_conflict: Optional[str] = None):
        self.conn = conn
        self.table_name = table_name
        self.data = data
        self.operation = operation
        self.on_conflict = on_conflict
    
    def execute(self):
        """Execute the insert/upsert."""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        columns = ', '.join(self.data.keys())
        placeholders = ', '.join(['%s'] * len(self.data))
        values = list(self.data.values())
        
        if self.operation == 'insert':
            query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders}) RETURNING *"
            cursor.execute(query, values)
        else:  # upsert
            # Determine conflict column - use on_conflict parameter or default to 'id' or 'url'
            conflict_col = self.on_conflict or ('url' if 'url' in self.data else 'id')
            update_clause = ', '.join([f"{k} = EXCLUDED.{k}" for k in self.data.keys() if k != conflict_col])
            query = f"""
                INSERT INTO {self.table_name} ({columns}) 
                VALUES ({placeholders})
                ON CONFLICT ({conflict_col}) DO UPDATE SET {update_clause}
                RETURNING *
            """
            cursor.execute(query, values)
        
        self.conn.commit()
        results = cursor.fetchall()
        cursor.close()
        return PostgresResult(results)


class PostgresRPCBuilder:
    """Builder for RPC/function calls that mimics Supabase client interface."""
    
    def __init__(self, conn, function_name: str, params: dict):
        self.conn = conn
        self.function_name = function_name
        self.params = params
    
    def execute(self):
        """Execute the RPC call."""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        # Build function call with named parameters
        # PostgreSQL functions use named parameters: function_name(param1 => value1, param2 => value2)
        if self.params:
            param_parts = [f"{k} => %s" for k in self.params.keys()]
            param_list = ', '.join(param_parts)
            query = f"SELECT * FROM {self.function_name}({param_list})"
            cursor.execute(query, list(self.params.values()))
        else:
            query = f"SELECT * FROM {self.function_name}()"
            cursor.execute(query)
        
        results = cursor.fetchall()
        cursor.close()
        return PostgresResult(results)


class PostgresResult:
    """Result wrapper compatible with Supabase client response."""
    
    def __init__(self, data):
        self.data = [dict(row) for row in data] if data else []

