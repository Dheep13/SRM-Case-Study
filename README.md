# GenAI Learning Resources & Agentic RAG Chatbot

An AI-powered system that discovers learning resources, tracks skill trends, and provides personalized career advice to IT students through an Agentic RAG chatbot.

## What This Does

**For IT Students:**
- Discover what skills are in-demand
- Get personalized learning roadmaps
- Find quality learning resources
- Track industry trends
- Chat with an AI advisor powered by real data

**How It Works:**
1. **AI Agents** discover resources from the web (GitHub, LinkedIn, articles)
2. **Supabase Database** stores resources and skills with vector embeddings
3. **Agentic RAG Chatbot** provides intelligent, personalized advice using multi-step reasoning

## Quick Start

### 🚀 Option 1: React Frontend (MAIN - Production Ready!)
```powershell
# Easy: Use the launcher
./start_dev.bat

# Or manually:
# Terminal 1: Start API
python api.py

# Terminal 2: Start React
cd frontend
npm run dev
```
Professional React interface at **http://localhost:5173** with:
- 💬 Interactive chatbot with Agentic RAG
- 🔍 AI-powered resource discovery
- 📊 Real-time analytics dashboard
- 📈 Interactive visualizations
- 📱 Fully responsive & mobile-friendly

### 🌐 Option 2: Streamlit (BACKUP - Quick Prototyping)
```powershell
streamlit run app.py
```
Simple interface at http://localhost:8501

### 💻 Option 3: Command Line

#### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Configure Environment
Copy `.env.example` to `.env` and add your keys:
```bash
OPENAI_API_KEY=your_openai_api_key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
TAVILY_API_KEY=your_tavily_api_key  # For web search
SERP_API_KEY=your_serp_api_key      # For trends
```

### 3. Setup Database
Go to Supabase Dashboard → SQL Editor and run:
1. `db_integration/schema.sql` - Creates tables
2. `db_integration/vector_embeddings.sql` - Enables vector search

### 4. Run the System

**Web Interface (Easy):**
```powershell
streamlit run app.py
```

**Command Line (Advanced):**
```powershell
# Discover resources and load to database
python load_and_visualize.py "GenAI skills for IT students"

# Generate embeddings (one-time)
python setup_chatbot.py

# Chat with the database
python chat_agentic.py
```

## Project Structure

```
Case Study/
├── agents/                      # Data discovery agents
│   ├── content_scraper_agent.py    # Web scraping
│   ├── trend_analysis_agent.py     # Trend tracking
│   └── orchestrator.py             # Coordinates agents
│
├── db_integration/              # Database & RAG system
│   ├── schema.sql                  # Database schema
│   ├── vector_embeddings.sql       # Vector search setup
│   ├── supabase_client.py          # Database operations
│   ├── agentic_rag.py              # Agentic RAG system
│   ├── chatbot.py                  # Simple chatbot
│   ├── skill_extractor.py          # AI skill extraction
│   ├── data_loader.py              # ETL pipeline
│   ├── embedding_manager.py        # Vector embeddings
│   ├── trend_analyzer.py           # Trend analysis
│   └── visualizer.py               # Chart generation
│
├── outputs/                     # Generated files
│   ├── charts/                     # PNG visualizations
│   └── reports/                    # JSON/TXT reports
│
├── Web Interface
│   ├── app.py                      # 🌐 Streamlit web UI (START HERE!)
│   └── run_app.bat                 # Windows launcher
│
├── Command Line Scripts
│   ├── load_and_visualize.py      # Full workflow
│   ├── chat_agentic.py             # Agentic RAG chatbot
│   ├── setup_chatbot.py            # Generate embeddings
│   └── config.py                   # Configuration
│
└── README.md                    # This file
```

## Architecture

### System Workflow

```
User Query
    ↓
┌─────────────────────────────────────────────┐
│ 1. Data Discovery (Agents)                 │
│    - Web scraping for resources             │
│    - GitHub/LinkedIn trend analysis         │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ 2. Data Storage (Supabase)                 │
│    - PostgreSQL database                    │
│    - Vector embeddings (pgvector)           │
│    - Skill extraction & categorization      │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ 3. Analysis & Visualization                │
│    - Trend analysis for students            │
│    - Demand scoring                         │
│    - Chart generation                       │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│ 4. Agentic RAG Chatbot                     │
│    - Intent analysis                        │
│    - Multi-step reasoning                   │
│    - Semantic search                        │
│    - Response refinement                    │
└─────────────────────────────────────────────┘
    ↓
Personalized Response
```

### What Makes This "Agentic" RAG?

**Traditional RAG** (Simple):
```
Query → Retrieve chunks → Stuff into LLM → Response
```

**Agentic RAG** (Our Approach):
```
Query
  → 1. Analyze Intent (LLM understands what you're asking)
  → 2. Plan Search Strategy (LLM decides what to search for)
  → 3. Retrieve Data (Semantic search with vector embeddings)
  → 4. Reason About Data (LLM analyzes and connects information)
  → 5. Draft Response (LLM creates initial answer)
  → 6. Refine Response (LLM improves clarity and accuracy)
  → 7. Verify Quality (Self-check before delivery)
Final Response
```

**Benefits:**
- Multi-step reasoning, not just chunk retrieval
- Self-improving responses
- Context-aware and personalized
- Higher quality answers

## Usage Guide

### 1. Discover New Resources

Run agents to find learning resources:
```powershell
python load_and_visualize.py "GenAI and ML skills"
```

**What it does:**
- Scrapes web for learning resources
- Analyzes GitHub/LinkedIn trends
- Extracts skills using AI
- Loads to Supabase
- Generates trend charts
- Creates student roadmaps

**Output:**
- `outputs/charts/` - 4 visualization charts
- `outputs/reports/` - JSON report with data

### 2. Chat with Database

Interactive chatbot with Agentic RAG:
```powershell
python chat_agentic.py
```

**Example queries:**
- "What skills should I learn as a Junior?"
- "Show me resources for learning Python"
- "What's trending in GenAI?"
- "Give me a 3-month learning plan"

**Features:**
- Multi-step reasoning
- Personalized for student level (Freshman → Graduate)
- Cites sources and demand scores
- Actionable recommendations

### 3. Generate Visualizations

Create charts for specific student levels:
```python
from db_integration.visualizer import SkillTrendVisualizer

viz = SkillTrendVisualizer()
viz.create_all_charts(student_level="Junior")
```

**Generates:**
1. `top_skills_chart.png` - Top 15 skills by demand
2. `category_distribution.png` - Skills by category
3. `skill_trends_timeline.png` - Trends over time
4. `student_roadmap.png` - Personalized learning path

## Database Schema

### Main Tables

**learning_resources**
- Stores discovered learning resources
- Fields: title, url, summary, category, source
- Linked to skills via junction table

**it_skills**
- IT skills with metadata
- Fields: skill_name, category, demand_score, student_level
- Automatically extracted by AI

**resource_skills**
- Junction table linking resources to skills

**skill_trends**
- Historical trend data
- Tracks demand over time

**resource_embeddings** & **skill_embeddings**
- Vector embeddings (1536 dimensions, OpenAI ada-002)
- Enables semantic search for chatbot

## Supabase Setup

### Step 1: Create Supabase Project
1. Go to https://supabase.com
2. Create new project
3. Copy URL and anon key to `.env`

### Step 2: Run SQL Schemas
In Supabase Dashboard → SQL Editor:

**A. Main Schema** (`db_integration/schema.sql`):
```sql
-- Creates tables:
-- - learning_resources
-- - it_skills
-- - trending_topics
-- - resource_skills
-- - skill_trends
```

**B. Vector Embeddings** (`db_integration/vector_embeddings.sql`):
```sql
-- Enables pgvector extension
-- Creates embedding tables:
-- - resource_embeddings
-- - skill_embeddings
-- - chat_history
```

### Step 3: Generate Embeddings
```powershell
python setup_chatbot.py
```

This converts all resources and skills to vector embeddings for semantic search.

## Configuration

### Environment Variables (.env)

```bash
# OpenAI API (required)
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo-preview

# Supabase (required for database)
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...

# Web Search (optional, for agent discovery)
TAVILY_API_KEY=tvly-...
SERP_API_KEY=...

# Agent Settings (optional)
MAX_RESOURCES=10
MAX_TOPICS=5
```

### config.py Settings

```python
# Agent behavior
MAX_RETRIES = 3
TIMEOUT = 30

# Database
BATCH_SIZE = 50

# Chatbot
TOP_K_RESULTS = 5  # Number of similar items to retrieve
STUDENT_LEVELS = ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"]
```

## API Keys Setup

### OpenAI (Required)
1. Go to https://platform.openai.com
2. Create API key
3. Add to `.env` as `OPENAI_API_KEY`

### Supabase (Required)
1. Project URL: Supabase Dashboard → Settings → API → URL
2. Anon Key: Supabase Dashboard → Settings → API → anon/public key
3. Add to `.env`

### Tavily (Optional - for better web search)
1. Go to https://tavily.com
2. Sign up and get API key
3. Add to `.env` as `TAVILY_API_KEY`

### SerpAPI (Optional - for trend analysis)
1. Go to https://serpapi.com
2. Sign up and get API key
3. Add to `.env` as `SERP_API_KEY`

## Troubleshooting

### Connection Issues
```
Error: Could not connect to Supabase
```
**Fix:** Check SUPABASE_URL and SUPABASE_KEY in `.env`

### Missing Tables
```
Error: Table 'learning_resources' not found
```
**Fix:** Run `db_integration/schema.sql` in Supabase SQL Editor

### No Embeddings
```
Error: No embeddings found
```
**Fix:** Run `python setup_chatbot.py` to generate embeddings

### Unicode/Encoding Errors
```
UnicodeEncodeError: 'charmap' codec...
```
**Fix:** This is a Windows terminal issue. Responses are saved to `outputs/reports/chatbot_response.txt`

### Rate Limits
```
Error: Rate limit exceeded (OpenAI)
```
**Fix:** 
- Wait a few minutes
- Reduce batch size in config.py
- Upgrade OpenAI plan

## Cost Estimates

### One-Time Setup
- Generate embeddings (100 items): ~$0.01
- Total: < $0.05

### Per Usage
- Run agents (10 resources): ~$0.10
- Chatbot query (simple): ~$0.01
- Chatbot query (agentic): ~$0.03-0.05
- Regenerate charts: $0 (no API calls)

### Monthly (Moderate Use)
- Weekly agent runs (4x): ~$0.40
- 50 chatbot queries: ~$1-2
- Supabase: Free tier sufficient
- **Total: < $3/month**

## Advanced Usage

### Custom Skill Extraction
```python
from db_integration.skill_extractor import SkillExtractor

extractor = SkillExtractor()
skills = extractor.extract_skills("Your text here")
```

### Trend Analysis
```python
from db_integration.trend_analyzer import TrendAnalyzer

analyzer = TrendAnalyzer()
trends = analyzer.analyze_for_student_level("Junior")
```

### Direct Database Queries
```python
from db_integration.supabase_client import SupabaseManager

db = SupabaseManager()
resources = db.get_all_resources(category="tutorial")
top_skills = db.get_top_skills(limit=10, category="AI/ML")
```

### Semantic Search
```python
from db_integration.embedding_manager import EmbeddingManager

em = EmbeddingManager()
results = em.semantic_search("machine learning", top_k=5)
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3.12 |
| **AI Framework** | LangGraph, LangChain |
| **LLM** | GPT-4 Turbo |
| **Embeddings** | OpenAI text-embedding-ada-002 |
| **Database** | Supabase (PostgreSQL) |
| **Vector Search** | pgvector |
| **Web Scraping** | Tavily, BeautifulSoup |
| **Visualization** | Matplotlib, Pandas |
| **Environment** | python-dotenv |

## Development

### Adding New Agents
Create new agent in `agents/` folder:
```python
from langgraph.graph import StateGraph

def my_agent(state):
    # Your logic
    return updated_state

# Register with orchestrator
```

### Adding Database Tables
1. Add schema to `db_integration/schema.sql`
2. Update `supabase_client.py` with new methods
3. Run schema in Supabase

### Customizing RAG
Edit `db_integration/agentic_rag.py`:
- Modify prompts in each step
- Adjust retrieval strategy
- Change reasoning approach

## Maintenance

### Weekly Tasks
```powershell
# Refresh data
python load_and_visualize.py "latest GenAI trends"
```

### Monthly Tasks
```powershell
# Regenerate embeddings if data changed significantly
python setup_chatbot.py

# Update dependencies
pip install -r requirements.txt --upgrade
```

### Cleanup
```powershell
# Clear old outputs
Remove-Item outputs\* -Recurse

# Files will regenerate on next run
```

## Contributing

This is an educational project. To extend:
1. Fork the repository
2. Add features in appropriate folders
3. Update tests in `archive/old_tests/` if needed
4. Keep documentation updated

## License

Educational project - use as needed for learning purposes.

## Contact & Support

For issues or questions:
- Check this README
- Review code comments
- Examine example usage in `examples/`

## Acknowledgments

Built using:
- LangChain & LangGraph for agentic workflows
- Supabase for backend infrastructure
- OpenAI for LLM and embeddings
- Tavily for web search capabilities

---

**Ready to help IT students discover their learning path!** 🚀

**Quick Commands:**
```powershell
# Full workflow
python load_and_visualize.py "your query"

# Chat with database
python chat_agentic.py

# View outputs
explorer outputs
```
