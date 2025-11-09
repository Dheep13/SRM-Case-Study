"""Supabase client for GenAI learning resources and trend analysis."""

import os
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Try to use database adapter if available, otherwise fall back to Supabase
try:
    from db_integration.database_adapter import DatabaseAdapter
    USE_ADAPTER = True
except ImportError:
    USE_ADAPTER = False


class SupabaseManager:
    """Manager for Supabase database operations."""
    
    def __init__(self):
        """Initialize Supabase client or PostgreSQL adapter."""
        # Check if we should use Docker PostgreSQL or Supabase
        use_supabase = os.getenv('USE_SUPABASE', 'false').lower() == 'true'
        
        if USE_ADAPTER and not use_supabase:
            # Use Docker PostgreSQL via adapter
            from db_integration.database_adapter import DatabaseAdapter
            adapter = DatabaseAdapter()
            self.client = adapter
            self.use_adapter = True
        else:
            # Use Supabase client (default or explicit)
            self.url = os.getenv('SUPABASE_URL')
            self.key = os.getenv('SUPABASE_KEY')
            
            if not self.url or not self.key:
                raise ValueError(
                    "SUPABASE_URL and SUPABASE_KEY must be set in .env file.\n"
                    "Get these from your Supabase project settings.\n"
                    "Or set USE_SUPABASE=false and configure DB_HOST, DB_NAME, etc. for Docker PostgreSQL."
                )
            
            self.client: Client = create_client(self.url, self.key)
            self.use_adapter = False
    
    # Learning Resources Operations
    
    def insert_learning_resource(self, resource: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a learning resource into the database.
        
        Args:
            resource: Resource data with title, url, description, etc.
            
        Returns:
            Inserted resource with ID
        """
        data = {
            'title': resource.get('title'),
            'url': resource.get('url'),
            'description': resource.get('description'),
            'category': resource.get('category', 'article'),
            'source': resource.get('source'),
            'relevance_score': resource.get('relevance_score', 0.5)
        }
        
        try:
            result = self.client.table('learning_resources').upsert(
                data,
                on_conflict='url'
            ).execute()
            return result.data[0] if result.data else {}
        except Exception as e:
            print(f"Error inserting resource: {e}")
            return {}
    
    def bulk_insert_resources(self, resources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Insert multiple learning resources.
        
        Args:
            resources: List of resource dictionaries
            
        Returns:
            List of inserted resources
        """
        inserted = []
        for resource in resources:
            result = self.insert_learning_resource(resource)
            if result:
                inserted.append(result)
        return inserted
    
    def get_all_resources(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all learning resources.
        
        Args:
            limit: Maximum number of resources to return
            
        Returns:
            List of resources
        """
        try:
            result = self.client.table('learning_resources')\
                .select('*')\
                .order('relevance_score', desc=True)\
                .limit(limit)\
                .execute()
            return result.data
        except Exception as e:
            print(f"Error fetching resources: {e}")
            return []
    
    # Trending Topics Operations
    
    def insert_trending_topic(self, topic: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a trending topic.
        
        Args:
            topic: Topic data with title, source, score, etc.
            
        Returns:
            Inserted topic with ID
        """
        data = {
            'title': topic.get('title'),
            'description': topic.get('description'),
            'source': topic.get('source'),
            'topic_type': topic.get('type'),
            'overall_score': topic.get('overall_score', 0),
            'metadata': topic.get('metrics', {})
        }
        
        try:
            result = self.client.table('trending_topics').insert(data).execute()
            return result.data[0] if result.data else {}
        except Exception as e:
            print(f"Error inserting topic: {e}")
            return {}
    
    def bulk_insert_topics(self, topics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Insert multiple trending topics.
        
        Args:
            topics: List of topic dictionaries
            
        Returns:
            List of inserted topics
        """
        inserted = []
        for topic in topics:
            result = self.insert_trending_topic(topic)
            if result:
                inserted.append(result)
        return inserted
    
    # IT Skills Operations
    
    def get_skill_by_name(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """Get a skill by name.
        
        Args:
            skill_name: Name of the skill
            
        Returns:
            Skill data or None
        """
        try:
            result = self.client.table('it_skills')\
                .select('*')\
                .eq('skill_name', skill_name)\
                .execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error fetching skill: {e}")
            return None
    
    def insert_skill(self, skill: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a new IT skill.
        
        Args:
            skill: Skill data
            
        Returns:
            Inserted skill
        """
        try:
            result = self.client.table('it_skills').insert(skill).execute()
            return result.data[0] if result.data else {}
        except Exception as e:
            print(f"Error inserting skill: {e}")
            return {}
    
    def get_top_skills(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get top IT skills by demand score.
        
        Args:
            limit: Number of skills to return
            
        Returns:
            List of top skills
        """
        try:
            result = self.client.table('it_skills')\
                .select('*')\
                .order('demand_score', desc=True)\
                .limit(limit)\
                .execute()
            return result.data
        except Exception as e:
            print(f"Error fetching top skills: {e}")
            return []
    
    def link_resource_to_skill(self, resource_id: str, skill_id: str, relevance: int = 5):
        """Link a resource to a skill.
        
        Args:
            resource_id: UUID of the resource
            skill_id: UUID of the skill
            relevance: Relevance score (1-10)
        """
        try:
            data = {
                'resource_id': resource_id,
                'skill_id': skill_id,
                'relevance': relevance
            }
            self.client.table('resource_skills').upsert(
                data,
                on_conflict='resource_id,skill_id'
            ).execute()
        except Exception as e:
            print(f"Error linking resource to skill: {e}")
    
    # Skill Trends Operations
    
    def insert_skill_trend(self, skill_id: str, trend_data: Dict[str, Any]):
        """Insert skill trend data.
        
        Args:
            skill_id: UUID of the skill
            trend_data: Trend metrics
        """
        data = {
            'skill_id': skill_id,
            'trend_date': trend_data.get('date', date.today().isoformat()),
            'mention_count': trend_data.get('mentions', 0),
            'resource_count': trend_data.get('resources', 0),
            'github_stars': trend_data.get('github_stars', 0),
            'linkedin_posts': trend_data.get('linkedin_posts', 0),
            'trend_score': trend_data.get('score', 0)
        }
        
        try:
            self.client.table('skill_trends').upsert(
                data,
                on_conflict='skill_id,trend_date'
            ).execute()
        except Exception as e:
            print(f"Error inserting skill trend: {e}")
    
    def get_skill_trends(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get skill trends for the last N days.
        
        Args:
            days: Number of days to look back
            
        Returns:
            List of trend data
        """
        try:
            result = self.client.table('skill_trends')\
                .select('*, it_skills(skill_name, category)')\
                .order('trend_date', desc=True)\
                .execute()
            return result.data
        except Exception as e:
            print(f"Error fetching skill trends: {e}")
            return []
    
    # Views and Analytics
    
    def get_top_skills_for_students(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get top skills for IT students from view.
        
        Args:
            limit: Number of skills to return
            
        Returns:
            List of top skills with analytics
        """
        try:
            result = self.client.table('top_skills_for_students')\
                .select('*')\
                .limit(limit)\
                .execute()
            return result.data
        except Exception as e:
            print(f"Error fetching top skills: {e}")
            return []
    
    def get_skill_trend_summary(self) -> List[Dict[str, Any]]:
        """Get skill trend summary from view.
        
        Returns:
            List of skill trends with summaries
        """
        try:
            result = self.client.table('skill_trend_summary')\
                .select('*')\
                .execute()
            return result.data
        except Exception as e:
            print(f"Error fetching trend summary: {e}")
            return []
    
    def get_recommended_learning_path(self, student_level: str) -> List[Dict[str, Any]]:
        """Get recommended learning path for a student level.
        
        Args:
            student_level: One of: Freshman, Sophomore, Junior, Senior, Graduate
            
        Returns:
            Recommended skills and learning paths
        """
        try:
            result = self.client.table('recommended_learning_path')\
                .select('*')\
                .eq('student_level', student_level)\
                .execute()
            return result.data
        except Exception as e:
            print(f"Error fetching learning path: {e}")
            return []
    
    # Student Recommendations
    
    def insert_recommendation(self, recommendation: Dict[str, Any]):
        """Insert a student recommendation.
        
        Args:
            recommendation: Recommendation data
        """
        try:
            self.client.table('student_recommendations').insert(recommendation).execute()
        except Exception as e:
            print(f"Error inserting recommendation: {e}")

