"""Test the AgenticRAGChatbot with your changes."""

import sys
import traceback

def test_chatbot():
    """Test the chatbot."""
    print("=" * 60)
    print("Testing AgenticRAGChatbot")
    print("=" * 60)
    
    try:
        print("\n[1/4] Importing AgenticRAGChatbot...")
        from db_integration.agentic_rag import AgenticRAGChatbot
        print("✅ Import successful")
        
        print("\n[2/4] Creating chatbot instance...")
        bot = AgenticRAGChatbot()
        print("✅ Bot created successfully")
        
        print("\n[3/4] Testing chat method...")
        response = bot.chat("What is Python?", "Junior")
        print(f"✅ Chat successful")
        print(f"Response length: {len(response)}")
        print(f"Response preview: {response[:200]}...")
        
        print("\n[4/4] Full response:")
        print("-" * 60)
        print(response)
        print("-" * 60)
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print("\n❌ Error occurred:")
        print("-" * 60)
        traceback.print_exc()
        print("-" * 60)
        sys.exit(1)

if __name__ == "__main__":
    test_chatbot()

