"""FastAPI backend for GenAI Learning Assistant React frontend."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="GenAI Learning Assistant API",
    description="API for AI-powered learning resource discovery and career guidance",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://genai-learning-assistant.cfapps.us10-001.hana.ondemand.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
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
    """Health check endpoint."""
    try:
        from db_integration.supabase_client import SupabaseManager
        db = SupabaseManager()
        return {
            "status": "healthy",
            "database": "connected",
            "embeddings": os.path.exists('.env')
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

# Chat endpoint
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with Agentic RAG bot."""
    try:
        from db_integration.agentic_rag import AgenticRAGChatbot
        
        bot = AgenticRAGChatbot()
        response = bot.chat(request.message, student_level=request.student_level)
        
        return ChatResponse(
            response=response,
            student_level=request.student_level
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

# Discovery endpoint
@app.post("/api/discover", response_model=DiscoveryResponse)
async def discover_resources(request: DiscoveryRequest):
    """Discover learning resources using AI agents."""
    try:
        from agents.orchestrator import GenAIAgentOrchestrator
        from db_integration.data_loader import DataLoader
        
        # Run agents
        orchestrator = GenAIAgentOrchestrator()
        report = orchestrator.run(request.query, output_format="json")
        
        # Load to database if requested
        stats = {}
        if request.load_to_db:
            loader = DataLoader()
            stats = loader.load_report(report)
        
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
        from db_integration.trend_analyzer import TrendAnalyzer
        
        db = SupabaseManager()
        analyzer = TrendAnalyzer()
        
        # Get trending skills for student level
        try:
            analysis = analyzer.get_student_skill_recommendations(student_level)
            # Transform the response to match our expected format
            trending_skills = analysis.get('immediate_focus', []) + analysis.get('next_to_learn', [])
        except Exception as e:
            print(f"Trend analysis error: {e}")
            trending_skills = []
            analysis = {}
        
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

