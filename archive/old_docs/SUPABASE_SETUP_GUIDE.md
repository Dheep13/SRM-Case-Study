# Quick Setup Guide: Supabase Integration for IT Student Skill Trends

## What This Does

This system helps IT college students discover what skills they should learn by:
1. Discovering GenAI learning resources automatically
2. Extracting and tracking IT skills from content
3. Analyzing trends to show what's hot in the industry
4. Creating visual charts of skill demand
5. Providing personalized learning roadmaps by student level

## Step-by-Step Setup

### Step 1: Set Up Supabase (5 minutes)

1. **Create Account**
   - Go to [supabase.com](https://supabase.com)
   - Click "Start your project"
   - Sign up with GitHub or email

2. **Create New Project**
   - Click "New Project"
   - Choose organization or create new one
   - Enter project name: `genai-skills-tracker`
   - Generate a strong password
   - Select region closest to you
   - Click "Create new project"
   - Wait 2-3 minutes for setup

3. **Get Your Credentials**
   - Once project is ready, go to Settings (gear icon)
   - Click "API" in left sidebar
   - Copy your:
     - Project URL (looks like: `https://xxxxx.supabase.co`)
     - Project API key (anon, public)

### Step 2: Configure Database (2 minutes)

1. **Open SQL Editor**
   - In Supabase dashboard, click "SQL Editor" (left sidebar)
   - Click "+ New query"

2. **Run Schema Script**
   - Open `supabase/schema.sql` from this project
   - Copy ALL the SQL code
   - Paste into Supabase SQL Editor
   - Click "Run" button
   - Wait for "Success" message

3. **Verify Tables Created**
   - Click "Table Editor" in left sidebar
   - You should see tables: `learning_resources`, `it_skills`, `trending_topics`, etc.

### Step 3: Configure Environment (1 minute)

1. **Update .env File**
   - Open your `.env` file
   - Add these lines:
   ```
   SUPABASE_URL=your_project_url_here
   SUPABASE_KEY=your_anon_key_here
   ```
   - Replace with your actual values from Step 1

2. **Install New Dependencies**
   ```powershell
   pip install supabase matplotlib pandas
   ```

### Step 4: Run the System (2 minutes)

**Option A: Complete Workflow (Recommended)**
```powershell
python load_and_visualize.py "GenAI skills for IT students"
```

This will:
- Discover learning resources
- Load data to Supabase
- Extract and analyze skills
- Generate 4 visualization charts

**Option B: Load Existing Report**
```powershell
python -c "from supabase.data_loader import DataLoader; DataLoader().load_from_json_file('test_report.json')"
```

### Step 5: View Results

**Charts Generated** (in project folder):
- `top_skills_chart.png` - Most in-demand skills
- `category_distribution.png` - Skills by category  
- `skill_trends_timeline.png` - Trends over time
- `student_roadmap.png` - Your learning path

**Database** (in Supabase):
- Go to Supabase → Table Editor
- Browse `it_skills`, `learning_resources`, `skill_trends`
- Use built-in filters and search

## Usage Examples

### For Sophomore Students
```python
from supabase.trend_analyzer import TrendAnalyzer

analyzer = TrendAnalyzer()
recommendations = analyzer.get_student_skill_recommendations("Sophomore")

print("Skills you should learn:")
for skill in recommendations['immediate_focus'][:5]:
    print(f"- {skill['skill_name']} ({skill['category']})")
```

### For Junior Students  
```python
from supabase.trend_analyzer import TrendAnalyzer

analyzer = TrendAnalyzer()
roadmap = analyzer.generate_learning_roadmap("Junior")

print("\nYour 6-Month Learning Plan:")
for phase, skills in roadmap['timeline'].items():
    print(f"\n{phase}:")
    for skill in skills[:3]:
        print(f"  - {skill.get('skill_name')}")
```

### Query Top Skills
```python
from supabase.supabase_client import SupabaseManager

db = SupabaseManager()
skills = db.get_top_skills_for_students(limit=10)

for i, skill in enumerate(skills, 1):
    print(f"{i}. {skill['skill_name']} - Demand: {skill['demand_score']}")
```

## Understanding the Results

### Demand Score (0-100)
- **90-100**: Extremely high demand, learn ASAP
- **70-89**: High demand, prioritize this
- **50-69**: Moderate demand, good to learn
- **Below 50**: Nice to have, not urgent

### Difficulty Levels
- **Beginner**: Good for Freshmen/Sophomores
- **Intermediate**: Good for Juniors
- **Advanced**: Good for Seniors/Graduates

### Skill Categories
- **AI/ML**: GenAI, LLMs, Machine Learning
- **Programming**: Languages and fundamentals
- **Web Development**: Frontend/Backend
- **Cloud**: AWS, Azure, Docker
- **Database**: SQL, NoSQL, Vector DBs
- **DevOps**: Git, CI/CD, Testing
- **Data Science**: Analysis, Visualization

## Keeping Data Fresh

Run weekly to update trends:
```powershell
python load_and_visualize.py "latest tech skills 2025"
```

## Troubleshooting

**"SUPABASE_URL not set"**
- Check `.env` file has correct credentials
- Restart terminal after editing `.env`

**"relation 'it_skills' does not exist"**
- Run `schema.sql` in Supabase SQL Editor
- Make sure all SQL executed successfully

**"No data for visualizations"**
- Load data first: `python load_and_visualize.py`
- Check Supabase has data: Table Editor → `it_skills`

**Charts not generating**
- Install matplotlib: `pip install matplotlib`
- Check for error messages in console

## What Students Get

1. **Current Market Insights**
   - See what skills companies actually want
   - Track emerging technologies early
   - Stay ahead of classmates

2. **Personalized Learning Path**
   - Recommendations for your year (Freshman → Senior)
   - Priority skills vs. nice-to-haves
   - Timeline: what to learn when

3. **Resource Discovery**
   - Curated learning materials
   - Courses, tutorials, documentation
   - Filtered by relevance and quality

4. **Visual Progress**
   - Charts showing industry trends
   - Category breakdown
   - Your personalized roadmap

5. **Data-Driven Decisions**
   - Stop guessing what to learn
   - Focus on high-demand skills
   - Maximize your learning ROI

## Example Output

```
Top 10 Skills for Junior Students:

1. Generative AI (AI/ML) - Demand: 95
2. Python (Programming) - Demand: 95  
3. LangChain (AI/ML) - Demand: 90
4. React (Web Development) - Demand: 88
5. RAG (AI/ML) - Demand: 88
6. Docker (Cloud) - Demand: 90
7. SQL (Database) - Demand: 90
8. Git (DevOps) - Demand: 95
9. Prompt Engineering (AI/ML) - Demand: 85
10. APIs (Programming) - Demand: 88

Your Learning Roadmap (Month 1-2):
  - Generative AI
  - Python
  - Git

Month 3-4:
  - LangChain
  - Docker
  - React
```

## Benefits

**For Students:**
- Know exactly what to learn and when
- Don't waste time on outdated skills
- Stand out in job interviews
- Build relevant portfolio

**For Career Planning:**
- Align learning with market demand
- Track emerging technologies
- Make informed specialization choices
- Prepare for internships/jobs

## Next Steps

1. ✅ Set up Supabase
2. ✅ Run the system
3. ✅ View your charts
4. 📚 Start learning top skills
5. 🔄 Update data weekly
6. 📈 Track your progress

## Advanced Usage

**Custom Queries**
```powershell
python load_and_visualize.py "machine learning frameworks 2025"
python load_and_visualize.py "web development trends"
python load_and_visualize.py "cloud computing skills"
```

**Focus on Specific Category**
```python
from supabase.trend_analyzer import TrendAnalyzer

analyzer = TrendAnalyzer()
ai_skills = analyzer.get_top_skills_by_category("AI/ML", limit=10)

for skill in ai_skills:
    print(f"{skill['skill_name']}: {skill['demand_score']}")
```

**Compare Student Levels**
```python
from supabase.trend_analyzer import TrendAnalyzer

analyzer = TrendAnalyzer()

for level in ["Sophomore", "Junior", "Senior"]:
    recs = analyzer.get_student_skill_recommendations(level)
    print(f"\n{level}: {len(recs['immediate_focus'])} skills to learn")
```

## Support

- 📖 Read `supabase/README.md` for detailed docs
- 🔍 Check Supabase dashboard for data
- 💬 Review error messages carefully
- 🐛 Most issues are configuration-related

---

**Ready to discover what skills you should learn? Run the system now!**

```powershell
python load_and_visualize.py
```

