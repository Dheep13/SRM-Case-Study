"""Complete workflow: Load data to Supabase and generate trend visualizations for IT students."""

import sys
import json
from agents.orchestrator import GenAIAgentOrchestrator
from db_integration.data_loader import DataLoader
from db_integration.trend_analyzer import TrendAnalyzer
from db_integration.visualizer import SkillTrendVisualizer


def main():
    """Main workflow for loading data and creating visualizations."""
    print("\n" + "#"*80)
    print("# GenAI Learning Resources - Supabase Integration & Trend Analysis")
    print("# For IT Students")
    print("#"*80)
    
    # Step 1: Get query from user or use default
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        print("\nEnter search query (or press Enter for default):")
        query = input("> ").strip()
        if not query:
            query = "GenAI and AI skills for IT students"
    
    print(f"\nQuery: {query}")
    
    # Step 2: Run GenAI agents to get learning resources
    print("\n" + "="*80)
    print("STEP 1: Discovering Learning Resources and Trends")
    print("="*80)
    
    try:
        orchestrator = GenAIAgentOrchestrator()
        report = orchestrator.run(query, output_format="json")
        
        print(f"\n[OK] Found {len(report['learning_resources'])} learning resources")
        print(f"[OK] Found {len(report['trending_topics'])} trending topics")
        
        # Save report
        report_file = "latest_report.json"
        orchestrator.save_report(report, report_file)
        
    except Exception as e:
        print(f"\n[ERROR] Failed to run agents: {e}")
        print("Trying to load from existing report file...")
        
        try:
            with open("test_report.json", "r") as f:
                report = json.load(f)
            print("[OK] Loaded existing report")
        except:
            print("[ERROR] No existing report found. Exiting.")
            return 1
    
    # Step 3: Load data to Supabase
    print("\n" + "="*80)
    print("STEP 2: Loading Data to Supabase")
    print("="*80)
    
    try:
        loader = DataLoader()
        stats = loader.load_report(report)
        
        print(f"\n[SUMMARY]")
        print(f"  Resources loaded: {stats['resources_loaded']}")
        print(f"  Topics loaded: {stats['topics_loaded']}")
        print(f"  Skills extracted: {stats['skills_extracted']}")
        print(f"  Resource-skill links: {stats['skills_linked']}")
        print(f"  Trend records: {stats['trends_created']}")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to load data to Supabase: {e}")
        print("\nPlease ensure:")
        print("1. Supabase project is set up")
        print("2. SUPABASE_URL and SUPABASE_KEY are configured in .env")
        print("3. Database schema is created (run schema.sql)")
        import traceback
        traceback.print_exc()
        return 1
    
    # Step 4: Analyze trends for IT students
    print("\n" + "="*80)
    print("STEP 3: Analyzing Trends for IT Students")
    print("="*80)
    
    try:
        analyzer = TrendAnalyzer()
        
        # Get recommendations for different student levels
        for level in ["Sophomore", "Junior", "Senior"]:
            print(f"\n--- {level} Students ---")
            recommendations = analyzer.get_student_skill_recommendations(level)
            
            print(f"Total skills analyzed: {recommendations['summary']['total_skills']}")
            print(f"Trending skills: {recommendations['summary']['trending_skills']}")
            
            print(f"\nImmediate Focus (Top 3):")
            for i, skill in enumerate(recommendations['immediate_focus'][:3], 1):
                print(f"  {i}. {skill.get('skill_name')} ({skill.get('category')})")
            
            print(f"\nNext to Learn (Top 3):")
            for i, skill in enumerate(recommendations['next_to_learn'][:3], 1):
                print(f"  {i}. {skill.get('skill_name')} ({skill.get('category')})")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to analyze trends: {e}")
        import traceback
        traceback.print_exc()
    
    # Step 5: Generate visualizations
    print("\n" + "="*80)
    print("STEP 4: Generating Trend Visualizations")
    print("="*80)
    
    try:
        visualizer = SkillTrendVisualizer()
        visualizer.create_all_charts(student_level="Junior")
        
        print("\nGenerated charts:")
        print("  1. top_skills_chart.png - Top skills by demand")
        print("  2. category_distribution.png - Skills by category")
        print("  3. skill_trends_timeline.png - Trends over time")
        print("  4. student_roadmap.png - Learning roadmap")
        
    except Exception as e:
        print(f"\n[ERROR] Failed to generate visualizations: {e}")
        import traceback
        traceback.print_exc()
    
    # Final summary
    print("\n" + "#"*80)
    print("# COMPLETE!")
    print("#"*80)
    print("\nResults:")
    print("  - Data loaded to Supabase database")
    print("  - Skill trends analyzed for IT students")
    print("  - Visualization charts generated")
    print("\nNext steps:")
    print("  1. View the generated PNG charts")
    print("  2. Query Supabase database for custom analysis")
    print("  3. Use the data to build a student dashboard")
    print(f"  4. Run again with different query: python load_and_visualize.py \"your query\"")
    
    return 0


if __name__ == "__main__":
    exit(main())

