from neo4j import GraphDatabase
import os

# Database Configuration
NEO4J_URI = 'neo4j+s://d8cff67c.databases.neo4j.io'
NEO4J_USERNAME = 'neo4j'
NEO4J_PASSWORD = '21T0Oi-LkNCH2JvcJ-8CUuh5AZsKSw6P1b7B5ZKHlRA'
NEO4J_DATABASE = 'neo4j'
AURA_INSTANCEID = 'd8cff67c'
AURA_INSTANCENAME = 'Instance02'

print("=" * 60)
print("NEO4J AURA CONNECTION TEST")
print("=" * 60)
print(f"Instance: {AURA_INSTANCENAME} ({AURA_INSTANCEID})")
print(f"URI: {NEO4J_URI}")
print(f"Username: {NEO4J_USERNAME}")
print(f"Database: {NEO4J_DATABASE}")
print("=" * 60)

# Create driver
driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
)

try:
    # Test connection
    print("\nTesting connection...")
    driver.verify_connectivity()
    print("✅ Connection successful!")
    
    # Run a simple test query
    with driver.session() as session:
        # Test basic query
        result = session.run("RETURN 'Connection to Instance02 successful!' as message")
        message = result.single()['message']
        print(f"✅ Query test successful: {message}")
        
        # Check database status
        result = session.run("MATCH (n) RETURN count(n) as count")
        node_count = result.single()['count']
        print(f"📊 Total nodes in database: {node_count}")
        
        # List node labels if any exist
        result = session.run("CALL db.labels() YIELD label RETURN label")
        labels = [record['label'] for record in result]
        if labels:
            print(f"📋 Node labels found: {', '.join(labels)}")
        else:
            print("📋 Database is empty (no node labels)")
        
        # Check if it's truly empty or has nodes without labels
        if node_count > 0 and not labels:
            print("   Note: Database has nodes but no labels defined")
        
        print("\n✅ Database is ready for use!")
        
except Exception as e:
    error_msg = str(e)
    print(f"\n❌ Connection failed: {error_msg}")
    
    if "Unable to retrieve routing information" in error_msg:
        print("\n🔍 DATABASE IS LIKELY PAUSED!")
        print("\nImmediate fix:")
        print("1. Go to https://console.neo4j.io/")
        print("2. Find 'Instance02' in your databases")
        print("3. If status is 'Paused', click 'Resume'")
        print("4. Wait 30-60 seconds for it to fully start")
        print("5. Run this script again")
    else:
        print("\n🔍 Other possible issues:")
        print("- Check if password is correct (try resetting in Aura console)")
        print("- Verify instance ID 'd8cff67c' is correct")
        print("- Check network/firewall settings for port 7687")
    
finally:
    driver.close()
    print("\n🔌 Connection test complete")
    print("=" * 60)