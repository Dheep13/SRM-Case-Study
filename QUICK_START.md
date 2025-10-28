# Quick Start Guide - Running Locally

## 🚀 EASIEST WAY: React Frontend (Recommended)

### Step 1: Setup Environment Variables

Create a `.env` file in the project root:

```powershell
# Copy the example file
copy .env.example .env

# Edit with your actual API keys
notepad .env
```

Add your API keys:
```
OPENAI_API_KEY=sk-...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...
TAVILY_API_KEY=tvly-...  (optional)
```

### Step 2: Install Python Dependencies

```powershell
pip install -r requirements.txt
```

### Step 3: Setup Database

Go to your Supabase Dashboard → SQL Editor and run these SQL files:

1. **First file**: `db_integration/schema.sql`
2. **Second file**: `db_integration/vector_embeddings.sql`

### Step 4: Generate Embeddings (One-time)

```powershell
python setup_chatbot.py
```

This processes existing data into embeddings for the chatbot.

### Step 5: Run the Application

**Option A: Using the automated launcher (EASIEST)**
```powershell
# Opens 2 windows: Backend API + React Frontend
.\start_dev.bat
```

**Option B: Manual (2 terminals)**

Terminal 1 - Backend API:
```powershell
python api.py
```

Terminal 2 - React Frontend:
```powershell
cd frontend
npm install  # First time only
npm run dev
```

### Step 6: Access the App

- **React Frontend**: http://localhost:5173
- **API Backend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## 🎯 ALTERNATIVE: Streamlit Interface (Simpler)

If you want a simpler web interface without React setup:

```powershell
# Run this single command
streamlit run app.py
```

Then open: **http://localhost:8501**

---

## 💡 What Each Interface Does

### React Frontend (start_dev.bat)
- Modern, professional UI
- Real-time chatbot
- Interactive analytics dashboard
- Resource discovery interface
- Beautiful visualizations

### Streamlit (app.py)
- Simple web interface
- Chat assistant
- Analytics view
- Trend charts
- Resource discovery

---

## 🗄️ Database Setup Details

### 1. Create Supabase Project
1. Go to https://supabase.com
2. Create a new project
3. Copy your project URL and anon key

### 2. Run SQL Schemas

In Supabase Dashboard → SQL Editor:

**A. Run schema.sql**
```sql
-- Copy and paste contents of db_integration/schema.sql
-- This creates all necessary tables
```

**B. Run vector_embeddings.sql**
```sql
-- Copy and paste contents of db_integration/vector_embeddings.sql
-- This enables vector search capabilities
```

### 3. Generate Initial Data (Optional)

```powershell
# Discover resources and load to database
python load_and_visualize.py "GenAI skills for IT students"
```

---

## 🔑 API Keys Setup

### Required Keys:

| Key | Purpose | Where to Get |
|-----|---------|--------------|
| `OPENAI_API_KEY` | AI features | https://platform.openai.com |
| `SUPABASE_URL` | Database | Supabase Dashboard |
| `SUPABASE_KEY` | Database auth | Supabase Dashboard |
| `TAVILY_API_KEY` | Web search | https://tavily.com |
| `GITHUB_TOKEN` | GitHub trends | https://github.com/settings/tokens |

### Optional Keys:
- `TAVILY_API_KEY` - For better web scraping
- `GITHUB_TOKEN` - For GitHub trend analysis
- `SERP_API_KEY` - For trend analysis (alternative to Tavily)

---

## ✅ Verify Everything Works

### 1. Check Backend Health
```powershell
curl http://localhost:8000/api/health
```

Should return:
```json
{
  "status": "healthy",
  "database": "connected",
  "embeddings": true
}
```

### 2. Check Frontend
Open http://localhost:5173 in browser

### 3. Test Chatbot
Ask: "What skills should I learn as a Junior?"

---

## 🐛 Troubleshooting

### "Module not found" errors
```powershell
pip install -r requirements.txt
```

### Database connection errors
- Verify SUPABASE_URL and SUPABASE_KEY in `.env`
- Check Supabase project is active

### "No embeddings found" errors
```powershell
python setup_chatbot.py
```

### Frontend won't start
```powershell
cd frontend
npm install
npm run dev
```

### Port already in use
```powershell
# Kill existing processes on ports 5173 or 8000
netstat -ano | findstr :5173
taskkill /PID <PID_NUMBER> /F

netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

---

## 📁 Project Structure

```
Case Study/
├── start_dev.bat          ← EASIEST: Run this!
├── run_app.bat            ← Alternative: Streamlit
├── .env                   ← Your API keys (create this)
│
├── frontend/              ← React UI
│   ├── package.json
│   └── src/
│
├── api.py                 ← FastAPI backend
├── app.py                 ← Streamlit alternative
│
├── agents/                ← AI agents
├── db_integration/        ← Database logic
└── requirements.txt       ← Python dependencies
```

---

## 🎯 Quick Commands Cheat Sheet

```powershell
# Start everything (React + API)
.\start_dev.bat

# Start Streamlit only
streamlit run app.py

# Generate embeddings
python setup_chatbot.py

# Discover resources
python load_and_visualize.py "your topic"

# Chat with database
python chat_agentic.py

# Install frontend dependencies
cd frontend
npm install

# View outputs
explorer outputs
```

---

## 🚨 Common First-Time Issues

### Issue 1: "No module named 'dotenv'"
**Fix**: `pip install -r requirements.txt`

### Issue 2: "Can't find .env file"
**Fix**: `copy .env.example .env` then edit with your keys

### Issue 3: "Database not connected"
**Fix**: 
1. Check SUPABASE_URL and SUPABASE_KEY in .env
2. Run the SQL schemas in Supabase

### Issue 4: "No embeddings found"
**Fix**: Run `python setup_chatbot.py`

### Issue 5: Frontend shows blank page
**Fix**: Make sure backend API is running on port 8000

---

## 🎉 You're Ready!

Once setup is complete:

1. **Discover Resources**: Use the "Discover" page to find learning materials
2. **Chat with AI**: Ask questions about skills and career paths
3. **View Analytics**: See trending skills and recommendations
4. **Generate Charts**: Create visualizations of skill trends

**Happy Learning!** 🚀


