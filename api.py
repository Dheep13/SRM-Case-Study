"""FastAPI backend for GenAI Learning Assistant React frontend."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import asyncio
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Thread pool for running blocking operations
# OPTIMIZED: Increased from 4 to 8 workers for better concurrency
executor = ThreadPoolExecutor(max_workers=8)

app = FastAPI(
    title="GenAI Learning Assistant API",
    description="API for AI-powered learning resource discovery and career guidance",
    version="1.0.0"
)

# CORS middleware for React frontend
# For production, add your public domain to allow_origins
# Example: "https://yourdomain.com", "https://www.yourdomain.com"
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "").split(",") if os.getenv("CORS_ORIGINS") else []
# Always allow localhost for development
default_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://genai-learning-assistant.cfapps.us10-001.hana.ondemand.com",
    "https://evolveiq-frontend.cfapps.us10-001.hana.ondemand.com"
]
# Combine default and custom origins, filter out empty strings
all_origins = default_origins + [origin.strip() for origin in CORS_ORIGINS if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=all_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    token: Optional[str] = None
    user: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    student_level: str = "Junior"

class VerifyTokenRequest(BaseModel):
    token: str

class ChatRequest(BaseModel):
    message: str
    student_level: str = "Junior"

class ChatResponse(BaseModel):
    response: str
    student_level: str

class DiscoveryRequest(BaseModel):
    query: str
    max_resources: int = 10
    load_to_db: bool = True

class DiscoveryResponse(BaseModel):
    resources: List[Dict[str, Any]]
    topics: List[Dict[str, Any]]
    stats: Dict[str, int]

class SkillsResponse(BaseModel):
    skills: List[Dict[str, Any]]
    total: int

class AnalyticsResponse(BaseModel):
    trending_skills: List[Dict[str, Any]]
    all_skills: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    stats: Dict[str, Any]

# Root endpoint - Commented out to serve React frontend at root
# Use /api/health to check API status instead
# @app.get("/")
# async def root():
#     """API root endpoint."""
#     return {
#         "message": "GenAI Learning Assistant API",
#         "version": "1.0.0",
#         "status": "active",
#         "endpoints": {
#             "chat": "/api/chat",
#             "discover": "/api/discover",
#             "skills": "/api/skills",
#             "analytics": "/api/analytics",
#             "charts": "/api/charts/generate"
#         }
#     }

# Health check
@app.get("/api/health")
async def health_check():
    """Health check endpoint - Must respond quickly for CF liveness checks."""
    # IMPORTANT: Keep this endpoint super lightweight
    # Cloud Foundry liveness checks timeout after 3 seconds
    return {
        "status": "healthy",
        "service": "evolveiq-api",
        "version": "1.0.0"
    }

# ==================== AUTHENTICATION ENDPOINTS ====================

@app.post("/api/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Login endpoint - verify username and password."""
    try:
        from db_integration.supabase_client import SupabaseManager
        import secrets
        from datetime import datetime, timedelta
        
        db = SupabaseManager()
        
        # Find user by username
        result = db.client.table('users').select('*').eq('username', request.username).execute()
        
        if not result.data or len(result.data) == 0:
            return LoginResponse(
                success=False,
                message="Invalid username or password"
            )
        
        user = result.data[0]
        
        # Verify password (simple comparison for now - in production use bcrypt)
        if user['password_hash'] != request.password:
            return LoginResponse(
                success=False,
                message="Invalid username or password"
            )
        
        # Check if user is active
        if not user.get('is_active', True):
            return LoginResponse(
                success=False,
                message="Account is disabled"
            )
        
        # Generate session token
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(days=7)  # 7 day session
        
        # Create session
        db.client.table('user_sessions').insert({
            'user_id': user['id'],
            'session_token': session_token,
            'expires_at': expires_at.isoformat()
        }).execute()
        
        # Update last login
        db.client.table('users').update({
            'last_login': datetime.now().isoformat()
        }).eq('id', user['id']).execute()
        
        # Return user info (without password)
        user_info = {
            'id': str(user['id']),
            'username': user['username'],
            'email': user.get('email'),
            'full_name': user.get('full_name'),
            'student_level': user.get('student_level', 'Junior')
        }
        
        return LoginResponse(
            success=True,
            token=session_token,
            user=user_info
        )
    except Exception as e:
        print(f"Login error: {e}")
        return LoginResponse(
            success=False,
            message=f"Login failed: {str(e)}"
        )

@app.post("/api/auth/verify")
async def verify_token(request: VerifyTokenRequest):
    """Verify session token and return user info."""
    try:
        from db_integration.supabase_client import SupabaseManager
        from datetime import datetime
        
        db = SupabaseManager()
        
        # Find session
        result = db.client.table('user_sessions').select('*').eq('session_token', request.token).execute()
        
        if not result.data or len(result.data) == 0:
            return {"valid": False, "message": "Invalid token"}
        
        session = result.data[0]
        
        # Check if expired
        expires_at_str = session['expires_at']
        if isinstance(expires_at_str, str):
            # Handle ISO format strings
            expires_at_str = expires_at_str.replace('Z', '+00:00')
            expires_at = datetime.fromisoformat(expires_at_str)
        else:
            expires_at = expires_at_str
        
        # Compare with current time (handle timezone-aware datetime)
        now = datetime.now(expires_at.tzinfo) if hasattr(expires_at, 'tzinfo') and expires_at.tzinfo else datetime.now()
        if expires_at < now:
            return {"valid": False, "message": "Token expired"}
        
        # Get user info
        user_result = db.client.table('users').select('*').eq('id', session['user_id']).execute()
        
        if not user_result.data or len(user_result.data) == 0:
            return {"valid": False, "message": "User not found"}
        
        user = user_result.data[0]
        
        # Update last activity
        db.client.table('user_sessions').update({
            'last_activity': datetime.now().isoformat()
        }).eq('id', session['id']).execute()
        
        # Return user info (without password)
        user_info = {
            'id': str(user.get('id')),
            'username': user.get('username'),
            'email': user.get('email'),
            'full_name': user.get('full_name'),
            'student_level': user.get('student_level', 'Junior')
        }
        
        return {
            "valid": True,
            "user": user_info
        }
    except Exception as e:
        import traceback
        print(f"Verify token error: {e}")
        print(traceback.format_exc())
        return {"valid": False, "message": str(e)}

@app.post("/api/auth/register", response_model=LoginResponse)
async def register(request: RegisterRequest):
    """Register a new user."""
    try:
        from db_integration.supabase_client import SupabaseManager
        import secrets
        from datetime import datetime, timedelta
        
        db = SupabaseManager()
        
        # Check if username already exists
        existing = db.client.table('users').select('id').eq('username', request.username).execute()
        if existing.data:
            return LoginResponse(
                success=False,
                message="Username already exists"
            )
        
        # Create user (password stored as-is for now - in production use bcrypt)
        user_data = {
            'username': request.username,
            'password_hash': request.password,  # In production, hash this
            'email': request.email,
            'full_name': request.full_name,
            'student_level': request.student_level,
            'is_active': True
        }
        
        result = db.client.table('users').insert(user_data).execute()
        
        if not result.data:
            return LoginResponse(
                success=False,
                message="Registration failed"
            )
        
        user = result.data[0]
        
        # Generate session token
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(days=7)
        
        # Create session
        db.client.table('user_sessions').insert({
            'user_id': user['id'],
            'session_token': session_token,
            'expires_at': expires_at.isoformat()
        }).execute()
        
        # Return user info
        user_info = {
            'id': str(user['id']),
            'username': user['username'],
            'email': user.get('email'),
            'full_name': user.get('full_name'),
            'student_level': user.get('student_level', 'Junior')
        }
        
        return LoginResponse(
            success=True,
            token=session_token,
            user=user_info
        )
    except Exception as e:
        print(f"Registration error: {e}")
        return LoginResponse(
            success=False,
            message=f"Registration failed: {str(e)}"
        )

@app.post("/api/auth/logout")
async def logout(request: Dict[str, Any]):
    """Logout - invalidate session token."""
    try:
        from db_integration.supabase_client import SupabaseManager
        
        db = SupabaseManager()
        token = request.get('token')
        
        if not token:
            return {"success": False, "message": "Token required"}
        
        # Delete session (ignore if already deleted)
        try:
            db.client.table('user_sessions').delete().eq('session_token', token).execute()
        except Exception:
            pass  # Session might already be deleted
        
        return {"success": True, "message": "Logged out successfully"}
    except Exception as e:
        return {"success": False, "message": str(e)}

# Chat endpoint
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with Agentic RAG bot - OPTIMIZED with timeout."""
    try:
        # Import here to avoid blocking startup
        from db_integration.agentic_rag import AgenticRAGChatbot

        # Define blocking function to run in thread
        def run_chat():
            bot = AgenticRAGChatbot()
            return bot.chat(request.message, student_level=request.student_level)

        # Run in thread pool - NO TIMEOUT, let it take as long as needed
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(executor, run_chat)

        return ChatResponse(
            response=response,
            student_level=request.student_level
        )
    except Exception as e:
        # Fallback to simple response if chatbot fails
        return ChatResponse(
            response=f"I'm sorry, I'm having trouble processing your request right now. Error: {str(e)}",
            student_level=request.student_level
        )

# Discovery endpoint
@app.post("/api/discover", response_model=DiscoveryResponse)
async def discover_resources(request: DiscoveryRequest):
    """Discover learning resources using AI agents - OPTIMIZED with timeout."""
    try:
        # Import here to avoid blocking startup
        from agents.orchestrator import GenAIAgentOrchestrator
        from db_integration.data_loader import DataLoader

        # Define blocking function to run in thread
        def run_discovery():
            # Run agents
            orchestrator = GenAIAgentOrchestrator()
            report = orchestrator.run(request.query, output_format="json")

            # Load to database if requested
            stats = {}
            if request.load_to_db:
                loader = DataLoader()
                stats = loader.load_report(report)

            return report, stats

        # Run in thread pool - NO TIMEOUT, let it take as long as needed
        loop = asyncio.get_event_loop()
        report, stats = await loop.run_in_executor(executor, run_discovery)

        return DiscoveryResponse(
            resources=report.get('learning_resources', []),
            topics=report.get('trending_topics', []),
            stats=stats if stats else {
                'resources_found': len(report.get('learning_resources', [])),
                'topics_found': len(report.get('trending_topics', []))
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Discovery error: {str(e)}")

# Skills endpoint
@app.get("/api/skills", response_model=SkillsResponse)
async def get_skills(category: Optional[str] = None, limit: int = 50):
    """Get IT skills from database."""
    try:
        from db_integration.supabase_client import SupabaseManager
        
        db = SupabaseManager()
        
        if category and category != "All Categories":
            skills = db.get_top_skills(category=category, limit=limit)
        else:
            skills = db.get_top_skills(limit=limit)
        
        return SkillsResponse(
            skills=skills,
            total=len(skills)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Skills error: {str(e)}")

# Analytics endpoint
@app.get("/api/analytics", response_model=AnalyticsResponse)
async def get_analytics(student_level: str = "Junior"):
    """Get analytics and recommendations."""
    try:
        from db_integration.supabase_client import SupabaseManager
        
        db = SupabaseManager()
        
        # Get trending skills using the view instead of TrendAnalyzer
        try:
            trending_skills = db.client.table('skill_trend_summary').select('*').limit(10).execute()
            trending_skills = trending_skills.data if trending_skills.data else []
        except Exception as e:
            print(f"Trend analysis error: {e}")
            trending_skills = []
        
        # Get all skills
        try:
            all_skills = db.get_top_skills(limit=100)
        except Exception as e:
            print(f"Get skills error: {e}")
            all_skills = []
        
        # Get resources
        try:
            resources = db.get_all_resources(limit=100)
        except Exception as e:
            print(f"Get resources error: {e}")
            resources = []
        
        # Calculate stats
        categories = {}
        for resource in resources:
            cat = resource.get('category', 'Other')
            categories[cat] = categories.get(cat, 0) + 1
        
        avg_demand = sum(s.get('demand_score', 0) for s in all_skills) / len(all_skills) if all_skills else 0
        
        return AnalyticsResponse(
            trending_skills=trending_skills[:10],
            all_skills=all_skills[:20],
            recommendations=trending_skills[:5],
            stats={
                'total_resources': len(resources),
                'total_skills': len(all_skills),
                'avg_demand': round(avg_demand, 1),
                'categories': categories
            }
        )
    except Exception as e:
        import traceback
        print(f"Analytics error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")

# Generate charts endpoint
@app.post("/api/charts/generate")
async def generate_charts(student_level: str = "Junior"):
    """Generate trend visualization charts."""
    try:
        from db_integration.visualizer import SkillTrendVisualizer
        import os
        from pathlib import Path
        
        viz = SkillTrendVisualizer()
        viz.create_all_charts(student_level=student_level)
        
        # Return paths to generated charts
        charts_dir = Path("outputs/charts")
        charts = []
        
        chart_files = [
            "top_skills_chart.png",
            "category_distribution.png",
            "skill_trends_timeline.png",
            "student_roadmap.png"
        ]
        
        for filename in chart_files:
            chart_path = charts_dir / filename
            if chart_path.exists():
                charts.append({
                    "name": filename.replace('.png', '').replace('_', ' ').title(),
                    "path": f"/charts/{filename}",
                    "filename": filename
                })
        
        return {
            "success": True,
            "charts": charts,
            "student_level": student_level
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chart generation error: {str(e)}")

# Get resources endpoint
@app.get("/api/resources")
async def get_resources(category: Optional[str] = None, limit: int = 50):
    """Get learning resources from database."""
    try:
        from db_integration.supabase_client import SupabaseManager
        
        db = SupabaseManager()
        
        if category and category != "All Categories":
            resources = db.client.table('learning_resources').select('*').eq('category', category).limit(limit).execute()
        else:
            resources = db.get_all_resources(limit=limit)
        
        return {
            "resources": resources if isinstance(resources, list) else resources.data,
            "total": len(resources if isinstance(resources, list) else resources.data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resources error: {str(e)}")

# Trending skills endpoint
@app.get("/api/trending-skills")
async def get_trending_skills(max_skills: int = 10, days_back: int = 30):
    """Get trending skills using real data from Tavily.
    
    Args:
        max_skills: Maximum number of trending skills to return
        days_back: How far back to analyze trends (default: 30 days)
    """
    try:
        from db_integration.trending_skills_analyzer import analyze_trending_skills
        
        def fetch_in_thread():
            return analyze_trending_skills(max_skills=max_skills, days_back=days_back)
        
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        trends = await loop.run_in_executor(executor, fetch_in_thread)
        
        return {
            "trends": trends,
            "total": len(trends),
            "source": "tech_community_analysis",
            "days_analyzed": days_back,
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Trending skills error: {e}")
        # Return empty list on error instead of failing
        return {
            "trends": [],
            "total": 0,
            "error": str(e)
        }

# Skill forecast endpoint
@app.get("/api/skill-forecast")
async def get_skill_forecast(max_skills: int = 10):
    """Get skill demand forecast using real job market data from Tavily.
    
    Args:
        max_skills: Maximum number of skills to return
    """
    try:
        from db_integration.skill_forecast_analyzer import analyze_skill_forecast
        
        def fetch_in_thread():
            return analyze_skill_forecast(max_skills=max_skills)
        
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        forecasts = await loop.run_in_executor(executor, fetch_in_thread)
        
        return {
            "forecasts": forecasts,
            "total": len(forecasts),
            "source": "job_market_analysis",
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Skill forecast error: {e}")
        # Return empty list on error instead of failing
        return {
            "forecasts": [],
            "total": 0,
            "error": str(e)
        }

# Tech news endpoint
@app.get("/api/tech-news")
async def get_tech_news(query: str = "AI technology artificial intelligence", limit: int = 10, days_back: int = 7):
    """Get latest tech news using Tavily API with date filtering.
    
    Args:
        query: Search query for tech news
        limit: Maximum number of articles to return
        days_back: How many days back to search (1, 7, 30, etc.)
    """
    try:
        from db_integration.tech_news_fetcher import fetch_tech_news
        
        def fetch_in_thread():
            return fetch_tech_news(query=query, max_results=limit, days_back=days_back)
        
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        news = await loop.run_in_executor(executor, fetch_in_thread)
        
        return {
            "news": news,
            "total": len(news),
            "query": query,
            "days_back": days_back
        }
    except Exception as e:
        print(f"Tech news error: {e}")
        # Return empty list on error instead of failing
        return {
            "news": [],
            "total": 0,
            "error": str(e)
        }

# ==================== ADMIN ENDPOINTS ====================

# Get all admin settings
@app.get("/api/admin/settings")
async def get_all_settings():
    """Get all configuration settings."""
    try:
        import json
        # Load from admin_config.json
        with open('admin_config.json', 'r') as f:
            config = json.load(f)
        
        # Apply database overrides if available
        try:
            from db_integration.supabase_client import SupabaseManager
            db = SupabaseManager()
            overrides = db.client.table('system_settings').select('*').execute()
            
            # Apply overrides
            for override in overrides.data:
                category = override.get('category')
                key = override.get('key')
                value = override.get('value')
                if category in config:
                    config[category][key] = value
        except:
            pass  # If no database, just use file config
        
        return config
    except Exception as e:
        # Return defaults if file doesn't exist
        return {
            "ai_models": {"llm_model": "gpt-4-turbo-preview", "temperature": 0.7, "max_tokens": 2000},
            "agents": {"content_scraper": {"enabled": True}, "trend_analyzer": {"enabled": True}},
            "trending": {"trending_threshold": 70, "mention_weight": 0.5, "github_weight": 0.3},
            "api_endpoints": {"tavily_enabled": True},
            "rag_workflow": {"enable_reasoning": True, "confidence_threshold": 0.7}
        }

# Update admin settings
@app.put("/api/admin/settings")
async def update_settings(settings: Dict[str, Any]):
    """Update configuration settings."""
    try:
        from db_integration.supabase_client import SupabaseManager
        import json
        
        db = SupabaseManager()
        
        # Save to database
        for category, values in settings.items():
            if isinstance(values, dict):
                for key, value in values.items():
                    # Handle nested config (like content_scraper)
                    if isinstance(value, dict):
                        for nested_key, nested_value in value.items():
                            db.client.table('system_settings').upsert({
                                'category': category,
                                'key': f"{key}.{nested_key}",
                                'value': json.dumps(nested_value) if isinstance(nested_value, (list, dict)) else nested_value,
                                'data_type': 'string' if isinstance(nested_value, str) else 
                                            'integer' if isinstance(nested_value, int) else
                                            'float' if isinstance(nested_value, float) else 'boolean'
                            }).execute()
                    else:
                        db.client.table('system_settings').upsert({
                            'category': category,
                            'key': key,
                            'value': json.dumps(value) if isinstance(value, (list, dict)) else value,
                            'data_type': 'string' if isinstance(value, str) else 
                                        'integer' if isinstance(value, int) else
                                        'float' if isinstance(value, float) else 'boolean'
                        }).execute()
        
        return {"status": "success", "message": "Settings updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update error: {str(e)}")

# Reset settings to defaults
@app.post("/api/admin/settings/reset")
async def reset_settings():
    """Reset all settings to defaults."""
    try:
        from db_integration.supabase_client import SupabaseManager
        db = SupabaseManager()
        
        # Delete all overrides from database
        db.client.table('system_settings').delete().neq('id', '00000000-0000-0000-0000-000000000000').execute()
        
        return {"status": "success", "message": "Settings reset to defaults"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reset error: {str(e)}")

# Get audit log
@app.get("/api/admin/audit-log")
async def get_audit_log(limit: int = 50):
    """Get configuration change audit log."""
    try:
        from db_integration.supabase_client import SupabaseManager
        db = SupabaseManager()
        
        result = db.client.table('config_audit_log').select('*').order('changed_at', desc=True).limit(limit).execute()
        
        return {"entries": result.data}
    except Exception as e:
        return {"entries": [], "error": str(e)}

# Admin health check
# Agent Access Control endpoints
@app.get("/api/admin/agent-access")
async def get_agent_access():
    """Get current agent access control configuration."""
    try:
        from agent_access_control import access_controller
        return access_controller.export_config()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting agent access config: {str(e)}")

@app.put("/api/admin/agent-access")
async def update_agent_access(config_data: Dict[str, Any]):
    """Update agent access control configuration."""
    try:
        from agent_access_control import access_controller
        success = access_controller.import_config(config_data)
        if success:
            return {"message": "Agent access configuration updated successfully"}
        else:
            raise HTTPException(status_code=400, detail="Invalid configuration data")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating agent access config: {str(e)}")

@app.get("/api/admin/agent-access/audit")
async def get_agent_access_audit(limit: int = 100):
    """Get audit log of agent access attempts."""
    try:
        from agent_access_control import access_controller
        audit_log = access_controller.get_audit_log(limit)
        return {"entries": audit_log}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting audit log: {str(e)}")

@app.post("/api/admin/agent-access/test")
async def test_agent_access(request: Dict[str, Any]):
    """Test agent access to a specific platform."""
    try:
        from agent_access_control import access_controller
        
        agent_name = request.get("agent_name")
        platform = request.get("platform")
        endpoint = request.get("endpoint")
        content_type = request.get("content_type")
        
        if not all([agent_name, platform, endpoint]):
            raise HTTPException(status_code=400, detail="Missing required parameters")
        
        allowed = access_controller.check_access(agent_name, platform, endpoint, content_type)
        return {
            "allowed": allowed,
            "agent": agent_name,
            "platform": platform,
            "endpoint": endpoint,
            "content_type": content_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error testing access: {str(e)}")

@app.get("/api/admin/health")
async def admin_health():
    """Admin system health check."""
    try:
        from db_integration.supabase_client import SupabaseManager
        import os
        
        db = SupabaseManager()
        
        # Check database connection using a table we know exists
        # Try learning_resources first (from main schema)
        try:
            db.client.table('learning_resources').select('id').limit(1).execute()
            database_status = "connected"
        except:
            # If learning_resources doesn't exist, try it_skills
            try:
                db.client.table('it_skills').select('id').limit(1).execute()
                database_status = "connected"
            except:
                database_status = "disconnected"
        
        # Check if config is loaded (env variables present)
        config_loaded = bool(os.getenv('OPENAI_API_KEY')) and bool(os.getenv('SUPABASE_URL'))
        
        return {
            "status": "healthy" if database_status == "connected" else "unhealthy",
            "database": database_status,
            "config_loaded": config_loaded
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "error",
            "config_loaded": False,
            "error": str(e)
        }

# Serve static files (charts)
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Mount outputs directory for serving charts (create if doesn't exist)
outputs_dir = Path("outputs")
charts_dir = outputs_dir / "charts"
if not charts_dir.exists():
    charts_dir.mkdir(parents=True, exist_ok=True)
    
if charts_dir.exists() and charts_dir.is_dir():
    app.mount("/charts", StaticFiles(directory="outputs/charts"), name="charts")

# Serve React frontend (for production deployment)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    @app.get("/{full_path:path}")
    async def serve_react(full_path: str):
        # Serve index.html for all non-API routes
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        
        file_path = os.path.join("static", full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=False)