"""Streamlit web interface for GenAI Learning Resources & Agentic RAG Chatbot."""

import streamlit as st
import os
from datetime import datetime
import json
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="GenAI Learning Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
    }
    .stat-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'student_level' not in st.session_state:
    st.session_state.student_level = "Junior"

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/000000/artificial-intelligence.png", width=150)
    st.markdown("### 🎓 GenAI Learning Assistant")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["🏠 Home", "💬 Chat Assistant", "🔍 Discover Resources", "📊 View Analytics", "📈 Trend Charts"]
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    student_level = st.selectbox(
        "Your Level",
        ["Freshman", "Sophomore", "Junior", "Senior", "Graduate"],
        index=2
    )
    st.session_state.student_level = student_level
    
    st.markdown("---")
    st.markdown("**Status:**")
    
    # Check if .env exists
    if os.path.exists('.env'):
        st.success("✓ Configuration OK")
    else:
        st.error("✗ Missing .env file")
    
    # Check database connection
    try:
        from db_integration.supabase_client import SupabaseManager
        db = SupabaseManager()
        st.success("✓ Database Connected")
    except:
        st.warning("⚠ Database Not Connected")

# Main content area
if page == "🏠 Home":
    st.markdown('<h1 class="main-header">🤖 GenAI Learning Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your AI-powered guide to learning IT skills and staying ahead of trends</p>', unsafe_allow_html=True)
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; color: white; text-align: center;">
            <h2>💬</h2>
            <h3>Chat Assistant</h3>
            <p>Get personalized advice from our Agentic RAG chatbot with multi-step reasoning</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 2rem; border-radius: 15px; color: white; text-align: center;">
            <h2>🔍</h2>
            <h3>Discover Resources</h3>
            <p>AI agents find the latest learning materials and trending topics</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 2rem; border-radius: 15px; color: white; text-align: center;">
            <h2>📊</h2>
            <h3>View Analytics</h3>
            <p>Explore skill trends, demand scores, and learning roadmaps</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick stats
    st.markdown("### 📈 Quick Statistics")
    
    try:
        from db_integration.supabase_client import SupabaseManager
        db = SupabaseManager()
        
        # Get stats
        resources = db.get_all_resources(limit=1000)
        skills = db.get_top_skills(limit=1000)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Learning Resources", len(resources))
        with col2:
            st.metric("IT Skills Tracked", len(skills))
        with col3:
            avg_demand = sum(s.get('demand_score', 0) for s in skills) / len(skills) if skills else 0
            st.metric("Avg Demand Score", f"{avg_demand:.1f}")
        with col4:
            st.metric("Your Level", st.session_state.student_level)
    except Exception as e:
        st.warning("Connect to database to see statistics")
    
    st.markdown("---")
    
    # Getting started
    st.markdown("### 🚀 Getting Started")
    
    with st.expander("1️⃣ Setup Database (One-time)"):
        st.code("""
# Run in Supabase SQL Editor:
1. db_integration/schema.sql
2. db_integration/vector_embeddings.sql

# Generate embeddings:
python setup_chatbot.py
        """)
    
    with st.expander("2️⃣ Discover Resources"):
        st.markdown("Go to **Discover Resources** page and enter a topic to search for learning materials")
    
    with st.expander("3️⃣ Chat with Assistant"):
        st.markdown("Go to **Chat Assistant** page and ask questions like:")
        st.markdown("- What skills should I learn as a Junior?")
        st.markdown("- Show me resources for learning Python")
        st.markdown("- What's trending in GenAI?")

elif page == "💬 Chat Assistant":
    st.markdown('<h1 class="main-header">💬 Chat Assistant</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">Agentic RAG-powered advice for {st.session_state.student_level} students</p>', unsafe_allow_html=True)
    
    # Chat interface
    st.markdown("### Ask me anything about IT skills and career paths!")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(f'<div class="chat-message user-message">👤 <strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot-message">🤖 <strong>Assistant:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Your question:", placeholder="e.g., What skills should I learn as a Junior?")
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            submit = st.form_submit_button("Send", use_container_width=True)
        with col2:
            clear = st.form_submit_button("Clear Chat", use_container_width=True)
    
    if clear:
        st.session_state.chat_history = []
        st.rerun()
    
    if submit and user_input:
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Get bot response
        with st.spinner("🤔 Thinking... (Using multi-step reasoning)"):
            try:
                from db_integration.agentic_rag import AgenticRAGChatbot
                
                bot = AgenticRAGChatbot()
                response = bot.chat(user_input, student_level=st.session_state.student_level)
                
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()
                
            except Exception as e:
                error_msg = f"Error: {str(e)}\n\nMake sure embeddings are generated: `python setup_chatbot.py`"
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
                st.rerun()

elif page == "🔍 Discover Resources":
    st.markdown('<h1 class="main-header">🔍 Discover Resources</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI agents will search the web for learning materials and trends</p>', unsafe_allow_html=True)
    
    # Discovery form
    with st.form("discovery_form"):
        query = st.text_input(
            "What do you want to learn?",
            placeholder="e.g., GenAI and ML skills for IT students"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            max_resources = st.slider("Max Resources", 5, 20, 10)
        with col2:
            load_to_db = st.checkbox("Load to Database", value=True)
        
        submit = st.form_submit_button("🚀 Discover", use_container_width=True)
    
    if submit and query:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Run agents
            status_text.text("Step 1/4: Running AI agents...")
            progress_bar.progress(25)
            
            from agents.orchestrator import GenAIAgentOrchestrator
            orchestrator = GenAIAgentOrchestrator()
            report = orchestrator.run(query, output_format="json")
            
            # Step 2: Show results
            status_text.text("Step 2/4: Processing results...")
            progress_bar.progress(50)
            
            st.success(f"✓ Found {len(report['learning_resources'])} resources and {len(report['trending_topics'])} topics!")
            
            # Display resources
            if report['learning_resources']:
                st.markdown("### 📚 Learning Resources")
                for i, resource in enumerate(report['learning_resources'][:5], 1):
                    with st.expander(f"{i}. {resource.get('title', 'Untitled')}"):
                        st.markdown(f"**Category:** {resource.get('category', 'N/A')}")
                        st.markdown(f"**Relevance:** {resource.get('relevance_score', 0):.2f}")
                        
                        # Display summary or description (handle different field names)
                        summary = resource.get('summary') or resource.get('description') or resource.get('content', 'No description available')
                        st.markdown(f"**Summary:** {summary}")
                        
                        url = resource.get('url', '')
                        if url:
                            st.markdown(f"[🔗 Visit]({url})")
                        
                        # Show any additional fields
                        if 'source' in resource:
                            st.markdown(f"*Source: {resource['source']}*")
            
            # Step 3: Load to database
            if load_to_db:
                status_text.text("Step 3/4: Loading to database...")
                progress_bar.progress(75)
                
                from db_integration.data_loader import DataLoader
                loader = DataLoader()
                stats = loader.load_report(report)
                
                st.success(f"✓ Loaded {stats['resources_loaded']} resources, {stats['skills_extracted']} skills to database!")
            
            # Step 4: Complete
            status_text.text("Step 4/4: Complete!")
            progress_bar.progress(100)
            
            st.balloons()
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Make sure your API keys are set in .env file")

elif page == "📊 View Analytics":
    st.markdown('<h1 class="main-header">📊 View Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Explore skill trends and demand analysis</p>', unsafe_allow_html=True)
    
    try:
        from db_integration.supabase_client import SupabaseManager
        from db_integration.trend_analyzer import TrendAnalyzer
        
        db = SupabaseManager()
        analyzer = TrendAnalyzer()
        
        # Top skills
        st.markdown("### 🏆 Top Skills by Demand")
        
        category_filter = st.selectbox(
            "Filter by Category",
            ["All Categories", "AI/ML", "Programming", "DevOps", "Database", "Cloud", "Web Development"]
        )
        
        if category_filter == "All Categories":
            skills = db.get_top_skills(limit=15)
        else:
            skills = db.get_top_skills(category=category_filter, limit=15)
        
        if skills:
            # Create a nice display
            for i, skill in enumerate(skills[:10], 1):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"**{i}. {skill['skill_name']}**")
                with col2:
                    st.metric("Demand", f"{skill['demand_score']}/100")
                with col3:
                    st.markdown(f"*{skill['category']}*")
        else:
            st.info("No skills found. Run discovery to populate the database.")
        
        st.markdown("---")
        
        # Trend analysis for student level
        st.markdown(f"### 📈 Recommended Skills for {st.session_state.student_level} Students")
        
        analysis = analyzer.analyze_for_student_level(st.session_state.student_level)
        
        if analysis['trending_skills']:
            st.markdown("#### 🔥 Immediate Focus")
            for skill in analysis['trending_skills'][:3]:
                st.markdown(f"- **{skill['skill_name']}** ({skill['category']}) - Demand: {skill['demand_score']}/100")
            
            if len(analysis['trending_skills']) > 3:
                st.markdown("#### 📚 Next to Learn")
                for skill in analysis['trending_skills'][3:6]:
                    st.markdown(f"- **{skill['skill_name']}** ({skill['category']}) - Demand: {skill['demand_score']}/100")
        
        st.markdown("---")
        
        # Resources by category
        st.markdown("### 📚 Resources by Category")
        
        resources = db.get_all_resources(limit=100)
        
        if resources:
            categories = {}
            for resource in resources:
                cat = resource.get('category', 'Other')
                categories[cat] = categories.get(cat, 0) + 1
            
            col1, col2 = st.columns(2)
            with col1:
                for cat, count in list(categories.items())[:len(categories)//2]:
                    st.metric(cat, count)
            with col2:
                for cat, count in list(categories.items())[len(categories)//2:]:
                    st.metric(cat, count)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.info("Make sure the database is set up and data is loaded")

elif page == "📈 Trend Charts":
    st.markdown('<h1 class="main-header">📈 Trend Charts</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Visual insights into skill demand and trends</p>', unsafe_allow_html=True)
    
    # Generate charts button
    if st.button("🎨 Generate Fresh Charts", use_container_width=True):
        with st.spinner("Generating visualizations..."):
            try:
                from db_integration.visualizer import SkillTrendVisualizer
                
                viz = SkillTrendVisualizer()
                viz.create_all_charts(student_level=st.session_state.student_level)
                
                st.success("✓ Charts generated successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    st.markdown("---")
    
    # Display charts
    charts_dir = Path("outputs/charts")
    
    if charts_dir.exists():
        chart_files = {
            "top_skills_chart.png": "🏆 Top Skills by Demand",
            "category_distribution.png": "📊 Skills by Category",
            "skill_trends_timeline.png": "📈 Skill Trends Over Time",
            "student_roadmap.png": f"🎓 Learning Roadmap for {st.session_state.student_level}"
        }
        
        for filename, title in chart_files.items():
            chart_path = charts_dir / filename
            if chart_path.exists():
                st.markdown(f"### {title}")
                st.image(str(chart_path), use_column_width=True)
                st.markdown("---")
            else:
                st.info(f"{title} not found. Click 'Generate Fresh Charts' above.")
    else:
        st.info("No charts available yet. Click 'Generate Fresh Charts' to create them.")
        st.markdown("Charts will be saved to `outputs/charts/` directory")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🤖 <strong>GenAI Learning Assistant</strong> - Powered by Agentic RAG & LangGraph</p>
    <p style="font-size: 0.9rem;">Built with Streamlit | Data stored in Supabase | Embeddings by OpenAI</p>
</div>
""", unsafe_allow_html=True)

