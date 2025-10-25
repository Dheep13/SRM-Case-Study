# Running the React Frontend

## Complete Professional Frontend Setup

Your project now has TWO frontends:
1. **React Frontend** (MAIN) - Professional production-ready UI  
2. **Streamlit** (BACKUP) - Quick prototyping interface

## Quick Start - React Frontend

### Step 1: Install FastAPI Dependencies
```powershell
pip install fastapi uvicorn
```

### Step 2: Start the API Backend
```powershell
python api.py
```
This starts the FastAPI backend at `http://localhost:8000`

### Step 3: Start React Frontend  
```powershell
cd frontend
npm run dev
```
This starts the React app at `http://localhost:5173`

### Step 4: Open Browser
Navigate to: `http://localhost:5173`

## What You Get

### React Frontend Features:
- ✨ Modern, professional UI with Tailwind CSS
- 🎨 Beautiful gradient designs
- 📱 Fully responsive (mobile-friendly)
- ⚡ Fast (Vite-powered)
- 🔄 Real-time updates
- 🎯 Production-ready architecture

### Pages:
1. **Home** - Dashboard with stats and quick actions
2. **Chat** - Interactive Agentic RAG chatbot
3. **Discover** - AI-powered resource discovery
4. **Analytics** - Skill trends and recommendations
5. **Charts** - Data visualizations

## Architecture

```
User Browser (localhost:5173)
    ↓ HTTP Requests
React Frontend
    ↓ API Calls (axios)
FastAPI Backend (localhost:8000)
    ↓ Function Calls
Python Backend
    ├── Agentic RAG (db_integration/)
    ├── AI Agents (agents/)
    └── Supabase Database
```

## API Endpoints

FastAPI serves these endpoints:

- `GET /` - API info
- `GET /api/health` - Health check
- `POST /api/chat` - Chat with AI
- `POST /api/discover` - Discover resources  
- `GET /api/skills` - Get skills
- `GET /api/analytics` - Get analytics
- `POST /api/charts/generate` - Generate charts
- `GET /api/resources` - Get resources

## Development Workflow

### Terminal 1 - Backend:
```powershell
python api.py
```

### Terminal 2 - Frontend:
```powershell
cd frontend
npm run dev
```

Both must be running simultaneously!

## Build for Production

### Backend:
```powershell
pip install -r requirements.txt
python api.py
```

### Frontend:
```powershell
cd frontend
npm run build
npm run preview
```

## Backup - Streamlit

If you prefer Streamlit:
```powershell
streamlit run app.py
```

## Troubleshooting

### Port Already in Use

**Backend (8000):**
```powershell
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Frontend (5173):**
React will automatically use next available port (5174, 5175, etc.)

### CORS Errors
Make sure both backend and frontend are running on correct ports:
- Backend: localhost:8000
- Frontend: localhost:5173

### API Not Found
Check that `api.py` is running and accessible at `http://localhost:8000`
Visit `http://localhost:8000/docs` for API documentation.

## Next Steps

1. Start both servers (backend + frontend)
2. Open `http://localhost:5173`
3. Try the chat feature
4. Discover resources
5. View analytics

**Your professional React frontend is ready!** 🚀

