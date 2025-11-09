# Project Structure - Docker Deployment

## 📁 Current Project Organization

```
Case Study/
│
├── 🐳 Docker Configuration
│   ├── Dockerfile                    # Backend container
│   ├── Dockerfile.combined           # Combined container (optional)
│   ├── docker-compose.yml           # Three-service setup (default)
│   ├── docker-compose.combined.yml  # Single-container setup (optional)
│   ├── docker-start.bat             # Windows startup script
│   ├── docker-start.sh              # Linux/Mac startup script
│   └── .dockerignore                # Docker build exclusions
│
├── 📚 Documentation
│   ├── README.md                     # Main project documentation
│   ├── DOCKER_DEPLOYMENT.md         # Complete Docker guide
│   ├── DOCKER_QUICK_START.md        # Quick reference
│   ├── DOCKER_SETUP_CHECKLIST.md    # Setup verification
│   ├── DOCKER_REVIEW_SUMMARY.md     # Review summary
│   ├── CLEANUP_SUMMARY.md           # Cleanup documentation
│   └── PROJECT_STRUCTURE.md          # This file
│
├── ⚙️ Configuration
│   ├── .env.example                  # Environment template
│   ├── .env.docker.example           # Docker environment template
│   ├── requirements.txt              # Python dependencies
│   └── admin_config.json             # Admin configuration
│
├── 🔧 Backend Application
│   ├── api.py                        # FastAPI main application
│   ├── app.py                        # Streamlit app (optional)
│   ├── config.py                     # Configuration
│   ├── config_manager.py             # Config management
│   ├── agent_access_control.py       # Access control
│   ├── setup_chatbot.py              # Chatbot setup
│   ├── load_and_visualize.py         # Data loading
│   ├── chat_agentic.py               # Chatbot CLI
│   │
│   ├── agents/                       # AI Agents
│   │   ├── orchestrator.py
│   │   ├── content_scraper_agent.py
│   │   └── trend_analysis_agent.py
│   │
│   ├── db_integration/               # Database Layer
│   │   ├── database_adapter.py      # PostgreSQL/Supabase adapter
│   │   ├── supabase_client.py        # Database client
│   │   ├── agentic_rag.py           # RAG system
│   │   ├── chatbot.py               # Chatbot logic
│   │   ├── data_loader.py           # Data loading
│   │   ├── embedding_manager.py     # Vector embeddings
│   │   ├── skill_extractor.py       # Skill extraction
│   │   ├── trend_analyzer.py        # Trend analysis
│   │   ├── visualizer.py            # Charts
│   │   ├── schema.sql               # Database schema
│   │   ├── vector_embeddings.sql    # Vector setup
│   │   └── admin_schema.sql         # Admin schema
│   │
│   └── models/                       # Data Models
│       └── admin_models.py
│
├── 🎨 Frontend Application
│   └── frontend/
│       ├── Dockerfile                # Frontend container
│       ├── nginx.conf                # Nginx configuration
│       ├── package.json              # Node dependencies
│       ├── vite.config.js            # Vite configuration
│       ├── tsconfig.json             # TypeScript config
│       ├── .dockerignore             # Docker exclusions
│       │
│       ├── src/                      # React Application
│       │   ├── App.jsx
│       │   ├── main.jsx
│       │   ├── pages/                # Page components
│       │   ├── components/           # Reusable components
│       │   └── utils/                # Utilities
│       │
│       ├── public/                   # Static assets
│       └── dist/                     # Build output (generated)
│
├── 📦 Examples
│   └── examples/
│       └── example_usage.py
│
└── 📦 Archive
    └── archive/
        ├── docker_migration/         # Archived CF files
        └── old_docs/                 # Old documentation
```

## 🗂️ File Categories

### Essential Files (Keep)
- All Docker configuration files
- Application source code
- Database schemas
- Current documentation
- Configuration templates

### Archived Files
- Cloud Foundry deployment files → `archive/docker_migration/cloud_foundry/`
- Old documentation → `archive/docker_migration/old_docs/`
- Old scripts → `archive/docker_migration/old_scripts/`
- Test files → `archive/docker_migration/test_files/`
- Frontend CF files → `archive/docker_migration/frontend_cf/`

## 🚀 Quick Start

1. **Copy environment file:**
   ```bash
   cp .env.docker.example .env
   ```

2. **Edit `.env` with your API keys**

3. **Start services:**
   ```bash
   docker-compose up -d
   ```

4. **Access:**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000
   - Database: localhost:5432

## 📝 Notes

- All Cloud Foundry files have been archived
- Project is now focused on Docker deployment
- Old documentation preserved for reference
- Clean, organized structure for easy navigation

