"""Setup script for chatbot with vector embeddings."""

import sys
from db_integration.embedding_manager import EmbeddingManager


def main():
    """Setup chatbot by generating embeddings."""
    print("\n" + "#"*80)
    print("# Chatbot Setup - Generate Vector Embeddings")
    print("#"*80)
    
    print("\nThis script will:")
    print("1. Generate embeddings for all learning resources")
    print("2. Generate embeddings for all IT skills")
    print("3. Enable semantic search for the chatbot")
    
    print("\nNote: This requires:")
    print("- OpenAI API key (for embeddings)")
    print("- Supabase configured with pgvector extension")
    print("- Data already loaded in database")
    
    response = input("\nContinue? (y/n): ").strip().lower()
    
    if response != 'y':
        print("\nSetup cancelled.")
        return 0
    
    try:
        # Generate embeddings
        manager = EmbeddingManager()
        stats = manager.generate_all_embeddings()
        
        print("\n" + "#"*80)
        print("# Setup Complete!")
        print("#"*80)
        
        print("\nYou can now use the chatbot:")
        print("  python chat_with_database.py")
        
        print("\nExample queries:")
        print("  - What skills should I learn?")
        print("  - Show me GenAI resources")
        print("  - What's trending in AI/ML?")
        
        return 0
    
    except Exception as e:
        print(f"\n✗ Setup failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you've run the vector_embeddings.sql script in Supabase")
        print("2. Ensure pgvector extension is enabled")
        print("3. Verify data is loaded: check learning_resources and it_skills tables")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())



