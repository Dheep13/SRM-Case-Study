# Web Interface Guide

## Simple Frontend for GenAI Learning Assistant

A beautiful web interface built with Streamlit that integrates all features:
- Agentic RAG Chatbot
- Resource Discovery
- Analytics Dashboard
- Trend Visualizations

## Quick Start

### Start the Web Interface

**Option 1: Double-click (Windows)**
```
run_app.bat
```

**Option 2: Command Line**
```powershell
streamlit run app.py
```

**Option 3: Python**
```powershell
python -m streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## Features

### 🏠 Home Page
- Overview of the system
- Quick statistics
- Getting started guide
- Feature highlights

### 💬 Chat Assistant
- Interactive chat interface
- Agentic RAG-powered responses
- Multi-step reasoning
- Personalized for student level
- Chat history maintained

**Example queries:**
- "What skills should I learn as a Junior?"
- "Show me resources for learning Python"
- "What's trending in GenAI?"
- "Give me a 3-month learning plan"

### 🔍 Discover Resources
- Search for learning materials
- AI agents scrape web in real-time
- Configure max resources
- Auto-load to database
- View discovered resources immediately

**How to use:**
1. Enter your topic (e.g., "GenAI skills")
2. Set max resources (5-20)
3. Choose to load to database
4. Click "Discover"
5. View results and resources

### 📊 View Analytics
- Top skills by demand
- Filter by category
- Personalized recommendations for your level
- Resource distribution
- Database statistics

**Shows:**
- Top 10 skills with demand scores
- Immediate focus skills for your level
- Next skills to learn
- Resources by category

### 📈 Trend Charts
- Visual insights
- Generate fresh charts on demand
- Auto-saves to outputs/charts/

**Charts included:**
1. Top Skills by Demand (bar chart)
2. Skills by Category (pie chart)
3. Skill Trends Timeline (line chart)
4. Learning Roadmap (personalized)

## Settings

### Student Level
Select your current level in the sidebar:
- Freshman
- Sophomore
- Junior
- Senior
- Graduate

This personalizes:
- Chat responses
- Skill recommendations
- Learning roadmaps
- Trend analysis

### Status Indicators
The sidebar shows:
- ✓ Configuration OK (if .env exists)
- ✓ Database Connected (if Supabase works)

## How It Integrates Everything

```
Web Interface (app.py)
    ↓
┌────────────────────────────────────┐
│ 1. Chat Assistant                 │
│    → db_integration/agentic_rag.py │
│    → Semantic search + LLM         │
└────────────────────────────────────┘
    ↓
┌────────────────────────────────────┐
│ 2. Discover Resources             │
│    → agents/orchestrator.py        │
│    → db_integration/data_loader.py │
└────────────────────────────────────┘
    ↓
┌────────────────────────────────────┐
│ 3. Analytics                      │
│    → db_integration/trend_analyzer │
│    → db_integration/supabase_client│
└────────────────────────────────────┘
    ↓
┌────────────────────────────────────┐
│ 4. Charts                         │
│    → db_integration/visualizer.py  │
│    → outputs/charts/               │
└────────────────────────────────────┘
```

## Technical Details

### Framework
- **Streamlit** - Python web framework
- Single-page app with navigation
- Real-time updates
- No frontend coding needed

### Pages
- `🏠 Home` - Overview and stats
- `💬 Chat Assistant` - Chatbot interface
- `🔍 Discover Resources` - Agent runner
- `📊 View Analytics` - Database insights
- `📈 Trend Charts` - Visualizations

### Session State
- Maintains chat history
- Remembers student level
- Persistent across interactions

### Styling
- Custom CSS for modern UI
- Gradient colors
- Responsive layout
- Mobile-friendly

## Customization

### Change Colors
Edit the CSS in `app.py`:
```python
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #YOUR_COLOR 0%, #YOUR_COLOR 100%);
    }
</style>
""", unsafe_allow_html=True)
```

### Add New Pages
```python
elif page == "🆕 New Page":
    st.markdown('<h1 class="main-header">🆕 New Page</h1>', unsafe_allow_html=True)
    # Your code here
```

### Modify Sidebar
Edit the sidebar section:
```python
with st.sidebar:
    # Add your widgets
    st.selectbox("New Option", [...])
```

## Deployment

### Local Network Access
Other devices on your network can access at:
```
http://YOUR_LOCAL_IP:8501
```

Find your IP:
```powershell
ipconfig
```
Look for "IPv4 Address"

### Cloud Deployment

**Streamlit Cloud (Free):**
1. Push code to GitHub
2. Go to streamlit.io/cloud
3. Connect repository
4. Deploy!

**Requirements for cloud:**
- Add secrets (API keys) in Streamlit dashboard
- Ensure requirements.txt is updated
- Add .streamlit/config.toml if needed

## Troubleshooting

### Port Already in Use
```
streamlit run app.py --server.port 8502
```

### Database Not Connected
- Check .env file exists
- Verify SUPABASE_URL and SUPABASE_KEY
- Run database schemas in Supabase

### Charts Not Showing
- Click "Generate Fresh Charts" button
- Check outputs/charts/ folder exists
- Ensure data is loaded in database

### Slow Response
- Normal for first query (cold start)
- Agentic RAG takes 5-15 seconds
- Check internet connection
- Verify OpenAI API key

## Tips

### Best Practices
1. **First Time:** Run discovery to populate database
2. **Chat:** Start with specific questions
3. **Analytics:** Check after adding new data
4. **Charts:** Regenerate after major updates

### Performance
- Keep browser tab open
- Refresh if UI becomes unresponsive
- Close other Streamlit instances
- Use latest browser version

### Data Management
- Discovery adds to database (doesn't replace)
- Chat doesn't modify data
- Charts can be regenerated anytime
- Clear outputs/charts/ to save space

## Screenshots

### Home Page
- Feature cards
- Quick stats
- Getting started

### Chat Interface
- Clean message bubbles
- User messages in blue
- Bot messages in purple
- Send and clear buttons

### Discovery Page
- Search input
- Progress bar
- Live results
- Expandable details

### Analytics Dashboard
- Metrics in cards
- Skill rankings
- Personalized recommendations

### Charts Page
- All 4 visualizations
- Full-width display
- Generate button

## Keyboard Shortcuts

- `Ctrl + R` - Rerun app
- `Ctrl + Shift + R` - Clear cache and rerun
- `Ctrl + K` - Command palette (Streamlit feature)

## Next Steps

1. **Customize** - Edit colors, add features
2. **Deploy** - Share with others on cloud
3. **Extend** - Add new pages/features
4. **Integrate** - Connect to other services

---

**Your GenAI Learning Assistant is now web-enabled!** 🚀

Access at: http://localhost:8501

