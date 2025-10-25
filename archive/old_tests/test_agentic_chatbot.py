"""Quick test of the Agentic RAG chatbot."""

from db_integration.agentic_rag import AgenticRAGChatbot

print("\n" + "="*80)
print("Testing Agentic RAG Chatbot")
print("="*80)

# Initialize chatbot
print("\nInitializing Agentic RAG system...")
bot = AgenticRAGChatbot()
print("[OK] System ready!\n")

# Test query
test_query = "What skills should I learn as a Junior student?"
print(f"Test Query: {test_query}\n")

# Get response
response = bot.chat(test_query, student_level="Junior")

print("\n" + "="*80)
print("Bot Response:")
print("="*80)
print(response)
print("\n" + "="*80)

print("\n[OK] Agentic RAG is working!")
print("\nTo chat interactively, run: python chat_agentic.py")

