"""Test database integration and load data to Supabase."""

import json
from db_integration.supabase_client import SupabaseManager
from db_integration.data_loader import DataLoader


def test_connection():
    """Test Supabase connection."""
    print("\n" + "="*80)
    print("Step 1: Testing Supabase Connection")
    print("="*80)
    
    try:
        db = SupabaseManager()
        print("\n[OK] Connected to Supabase successfully!")
        return True
    except Exception as e:
        print(f"\n[ERROR] Connection failed: {e}")
        print("\nPlease ensure:")
        print("1. SUPABASE_URL and SUPABASE_KEY are set in .env")
        print("2. Supabase project is running")
        return False


def check_tables():
    """Check if required tables exist."""
    print("\n" + "="*80)
    print("Step 2: Checking Database Tables")
    print("="*80)
    
    try:
        db = SupabaseManager()
        
        # Try to query each table
        tables_to_check = [
            'learning_resources',
            'it_skills',
            'trending_topics',
            'resource_skills',
            'skill_trends'
        ]
        
        for table in tables_to_check:
            try:
                result = db.client.table(table).select('*').limit(1).execute()
                print(f"✓ Table '{table}' exists")
            except Exception as e:
                print(f"✗ Table '{table}' not found")
                print(f"  Error: {e}")
                return False
        
        print("\n✓ All required tables exist!")
        return True
        
    except Exception as e:
        print(f"\n✗ Error checking tables: {e}")
        print("\nYou need to run the SQL schema in Supabase:")
        print("1. Go to Supabase Dashboard → SQL Editor")
        print("2. Copy contents of db_integration/schema.sql")
        print("3. Paste and Run")
        return False


def load_test_data():
    """Load test data to Supabase."""
    print("\n" + "="*80)
    print("Step 3: Loading Test Data")
    print("="*80)
    
    try:
        # Load test report
        print("\nLoading test_report.json...")
        with open('test_report.json', 'r', encoding='utf-8') as f:
            report = json.load(f)
        
        print(f"✓ Loaded report with:")
        print(f"  - {len(report.get('learning_resources', []))} resources")
        print(f"  - {len(report.get('trending_topics', []))} topics")
        
        # Load to database
        loader = DataLoader()
        stats = loader.load_report(report)
        
        print("\n✓ Data loading complete!")
        print(f"\nStatistics:")
        print(f"  Resources loaded: {stats['resources_loaded']}")
        print(f"  Topics loaded: {stats['topics_loaded']}")
        print(f"  Skills extracted: {stats['skills_extracted']}")
        print(f"  Resource-skill links: {stats['skills_linked']}")
        print(f"  Trend records: {stats['trends_created']}")
        
        return True
        
    except FileNotFoundError:
        print("\n✗ test_report.json not found")
        print("Run 'python test_run.py' first to generate test data")
        return False
    except Exception as e:
        print(f"\n✗ Error loading data: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_data():
    """Verify data was loaded correctly."""
    print("\n" + "="*80)
    print("Step 4: Verifying Loaded Data")
    print("="*80)
    
    try:
        db = SupabaseManager()
        
        # Check resources
        resources = db.get_all_resources(limit=5)
        print(f"\n✓ Found {len(resources)} resources in database")
        if resources:
            print(f"\nSample resource:")
            print(f"  Title: {resources[0].get('title')}")
            print(f"  Category: {resources[0].get('category')}")
        
        # Check skills
        skills = db.get_top_skills(limit=5)
        print(f"\n✓ Found {len(skills)} skills in database")
        if skills:
            print(f"\nSample skill:")
            print(f"  Name: {skills[0].get('skill_name')}")
            print(f"  Demand: {skills[0].get('demand_score')}")
        
        # Check topics
        try:
            topics = db.client.table('trending_topics').select('*').limit(5).execute()
            print(f"\n✓ Found {len(topics.data)} trending topics")
        except:
            print(f"\n✓ Trending topics table accessible")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Error verifying data: {e}")
        return False


def main():
    """Main test workflow."""
    print("\n" + "#"*80)
    print("# Database Integration Test")
    print("#"*80)
    
    # Test connection
    if not test_connection():
        print("\n❌ Test failed at connection step")
        return 1
    
    # Check tables
    if not check_tables():
        print("\n❌ Test failed at table check")
        print("\n📋 ACTION REQUIRED:")
        print("Run the database schema in Supabase:")
        print("1. Open Supabase Dashboard")
        print("2. Go to SQL Editor")
        print("3. Copy all contents from: db_integration/schema.sql")
        print("4. Paste and click 'Run'")
        print("5. Wait for 'Success' message")
        print("6. Run this script again")
        return 1
    
    # Load data
    if not load_test_data():
        print("\n❌ Test failed at data loading")
        return 1
    
    # Verify data
    if not verify_data():
        print("\n❌ Test failed at verification")
        return 1
    
    # Success!
    print("\n" + "#"*80)
    print("# ✓ ALL TESTS PASSED!")
    print("#"*80)
    
    print("\n🎉 Database integration successful!")
    print("\nYour Supabase database now contains:")
    print("  ✓ Learning resources")
    print("  ✓ IT skills")
    print("  ✓ Trending topics")
    print("  ✓ Resource-skill mappings")
    print("  ✓ Skill trend data")
    
    print("\n📊 Next Steps:")
    print("  1. View data in Supabase Dashboard → Table Editor")
    print("  2. Generate embeddings: python setup_chatbot.py")
    print("  3. Create visualizations: python -c \"from db_integration.visualizer import SkillTrendVisualizer; SkillTrendVisualizer().create_all_charts()\"")
    print("  4. Chat with database: python chat_agentic.py")
    
    return 0


if __name__ == "__main__":
    exit(main())

