# Supabase Integration for IT Student Skill Trends

This module integrates GenAI learning resources with Supabase to provide trend analysis and visualizations for IT students.

## Features

- **Data Storage**: Store learning resources and trending topics in Supabase
- **Skill Extraction**: Automatically extract IT skills from content
- **Trend Analysis**: Track skill popularity and demand over time
- **Student Recommendations**: Personalized skill recommendations by student level
- **Visualizations**: Generate charts showing skill trends and learning roadmaps

## Database Schema

The system uses the following tables:
- `learning_resources` - Stores discovered learning content
- `trending_topics` - Tracks trending topics from GitHub/LinkedIn
- `it_skills` - Master list of IT skills
- `resource_skills` - Links resources to skills
- `skill_trends` - Time-series data of skill popularity
- `student_recommendations` - Curated recommendations by level

## Setup

### 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Note your project URL and anon key

### 2. Run Database Schema

In your Supabase project:
1. Go to SQL Editor
2. Copy contents of `supabase/schema.sql`
3. Run the SQL to create tables, views, and functions

### 3. Configure Environment

Add to your `.env` file:
```
SUPABASE_URL=your_project_url
SUPABASE_KEY=your_anon_key
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

## Usage

### Complete Workflow

Run the full workflow to discover resources, load to Supabase, and generate visualizations:

```powershell
python load_and_visualize.py "GenAI skills for IT students"
```

This will:
1. Run GenAI agents to discover learning resources
2. Load data to Supabase
3. Extract and categorize skills
4. Analyze trends for IT students
5. Generate visualization charts

### Individual Components

**Load Data Only:**
```python
from supabase.data_loader import DataLoader

loader = DataLoader()
stats = loader.load_from_json_file("test_report.json")
```

**Analyze Trends:**
```python
from supabase.trend_analyzer import TrendAnalyzer

analyzer = TrendAnalyzer()
recommendations = analyzer.get_student_skill_recommendations("Junior")
```

**Generate Visualizations:**
```python
from supabase.visualizer import SkillTrendVisualizer

visualizer = SkillTrendVisualizer()
visualizer.create_all_charts(student_level="Junior")
```

## Skill Categories

The system tracks skills in these categories:
- **AI/ML** - GenAI, LLMs, LangChain, RAG, Embeddings
- **Programming** - Python, JavaScript, TypeScript, Data Structures
- **Web Development** - React, Node.js, APIs, Frontend/Backend
- **Cloud** - AWS, Azure, Docker, Kubernetes
- **Database** - SQL, PostgreSQL, MongoDB, Vector DBs
- **DevOps** - Git, CI/CD, Testing, Deployment
- **Data Science** - pandas, Analysis, Visualization
- **Mobile** - iOS, Android, React Native

## Student Levels

Recommendations are tailored for:
- **Freshman** - Focus on fundamentals
- **Sophomore** - Building core skills
- **Junior** - Intermediate to advanced skills
- **Senior** - Advanced skills and specialization
- **Graduate** - Cutting-edge and research skills

## Generated Visualizations

### 1. Top Skills Chart
Horizontal bar chart showing top skills by demand score

### 2. Category Distribution
Pie chart showing skill distribution across categories

### 3. Skill Trends Timeline
Line chart tracking skill popularity over time

### 4. Student Roadmap
Learning timeline and priority skills for specific student level

## Database Views

Pre-built views for common queries:

**top_skills_for_students**
```sql
SELECT * FROM top_skills_for_students LIMIT 20;
```

**skill_trend_summary**
```sql
SELECT * FROM skill_trend_summary WHERE avg_trend_score > 70;
```

**recommended_learning_path**
```sql
SELECT * FROM recommended_learning_path WHERE student_level = 'Junior';
```

## API Examples

### Query Top Skills
```python
from supabase.supabase_client import SupabaseManager

db = SupabaseManager()
top_skills = db.get_top_skills(limit=20)

for skill in top_skills:
    print(f"{skill['skill_name']}: {skill['demand_score']}")
```

### Get Learning Path
```python
from supabase.trend_analyzer import TrendAnalyzer

analyzer = TrendAnalyzer()
roadmap = analyzer.generate_learning_roadmap("Junior")

for phase, skills in roadmap['timeline'].items():
    print(f"\n{phase}:")
    for skill in skills:
        print(f"  - {skill.get('skill_name')}")
```

### Track Skill Trends
```python
import pandas as pd
from supabase.trend_analyzer import TrendAnalyzer

analyzer = TrendAnalyzer()
df = analyzer.get_skill_growth_data(days=30)

# Analyze trends
print(df.groupby('skill_name')['trend_score'].mean().nlargest(10))
```

## Customization

### Add New Skills

Edit `supabase/skill_extractor.py` to add skills to `IT_SKILLS_TAXONOMY`:

```python
IT_SKILLS_TAXONOMY = {
    'AI/ML': [
        'Generative AI',
        'Your New Skill',
        # ... more skills
    ]
}
```

### Modify Difficulty Levels

Update `categorize_difficulty()` in `skill_extractor.py` to customize difficulty classification.

### Custom Visualizations

Extend `SkillTrendVisualizer` class to create custom charts.

## Troubleshooting

**Error: SUPABASE_URL not set**
- Add Supabase credentials to `.env` file

**Error: relation does not exist**
- Run `schema.sql` in Supabase SQL Editor

**No data for visualizations**
- Load data first using `load_and_visualize.py`
- Ensure resources have been inserted into database

**Import errors**
- Install dependencies: `pip install -r requirements.txt`

## Benefits for IT Students

1. **Data-Driven Learning** - See what skills are actually in demand
2. **Personalized Roadmap** - Get recommendations for your level
3. **Trend Awareness** - Stay updated on emerging technologies
4. **Resource Discovery** - Find quality learning materials
5. **Career Preparation** - Focus on skills employers want

## Future Enhancements

- Real-time trend updates
- Job market integration
- Skill gap analysis
- Course recommendations
- Community feedback system
- Mobile app integration

## Architecture

```
User Query
    ↓
GenAI Agents (Discover Resources)
    ↓
Skill Extractor (Extract Skills)
    ↓
Supabase Database (Store & Analyze)
    ↓
Trend Analyzer (Generate Insights)
    ↓
Visualizer (Create Charts)
    ↓
Student Dashboard
```

## Files

- `schema.sql` - Database schema
- `supabase_client.py` - Database client
- `skill_extractor.py` - Skill extraction logic
- `data_loader.py` - Data loading pipeline
- `trend_analyzer.py` - Trend analysis
- `visualizer.py` - Chart generation
- `README.md` - This file

## Support

For issues or questions:
1. Check this README
2. Review error messages
3. Verify Supabase configuration
4. Check that schema is properly created

