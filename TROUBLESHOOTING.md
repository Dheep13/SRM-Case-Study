# Troubleshooting Guide

## Red Blinking Dot in Frontend

This indicates the backend API server is not running or not accessible.

### Solution 1: Start the API Server

```bash
python api.py
```

Wait for: `INFO: Application startup complete.`

### Solution 2: Check Environment Variables

Ensure `.env` file exists with:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key
OPENAI_API_KEY=your_openai_key
```

### Solution 3: Database Tables Missing

The admin configuration system requires additional tables. Run this in Supabase SQL Editor:

```
File: db_integration/admin_schema.sql
```

This creates:
- `system_settings` table
- `admin_users` table  
- `config_audit_log` table

### Solution 4: Port Conflicts

If port 8000 is in use:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID [PID] /F

# Or use different port
set PORT=8001
python api.py
```

### Solution 5: Frontend Can't Connect

If frontend at `http://localhost:5173` can't reach API:

1. Check API is running: `curl http://localhost:8000/api/health`
2. Check CORS settings in `api.py`
3. Restart both servers

## Database Connection Issues

### Error: "SUPABASE_URL and SUPABASE_KEY must be set"

**Fix**: Create `.env` file with your credentials

```bash
# Copy example file
copy .env.example .env

# Edit with your keys
notepad .env
```

### Error: "relation does not exist"

**Fix**: Run schema files in Supabase:

1. Go to Supabase Dashboard → SQL Editor
2. Run `db_integration/schema.sql`
3. Run `db_integration/admin_schema.sql`

## Admin Features Not Working

### Admin Mode Won't Enable

**Fix**: Double-click the logo in navbar, or manually:
```javascript
localStorage.setItem('isAdmin', 'true')
```

### Settings Not Saving

**Fix**: Check that `system_settings` table exists:
```sql
-- Run in Supabase SQL Editor
SELECT * FROM system_settings LIMIT 1;
```

If empty or error, run `admin_schema.sql` again.

## Trending Skills Not Showing

### Issue: No skills in "Trending" section

**Fix 1**: Lower the trending threshold
- Open Settings Modal (⚙️ icon)
- Go to Trending tab
- Change threshold from 70 to 60
- Save

**Fix 2**: Run discovery to populate data
```bash
python load_and_visualize.py "GenAI skills for students"
```

**Fix 3**: Check if data exists
```python
from db_integration.supabase_client import SupabaseManager
db = SupabaseManager()
skills = db.get_top_skills(limit=10)
print(f"Found {len(skills)} skills")
```

## Quick Health Check

Run this to test everything:

```bash
# 1. Test database connection
python -c "from db_integration.supabase_client import SupabaseManager; db = SupabaseManager(); print('DB OK')"

# 2. Start API
python api.py

# 3. In another terminal, start frontend
cd frontend
npm run dev

# 4. Access
# Frontend: http://localhost:5173
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Common Error Messages

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Port already in use"
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID [number] /F
```

### "Authentication failed"
Check SUPABASE_KEY in `.env` is correct

### "Table does not exist"
Run `db_integration/schema.sql` in Supabase

