"""Agentic RAG chatbot CLI - Multi-step reasoning with LLM refinement."""

import sys
from db_integration.agentic_rag import AgenticRAGChatbot


def print_banner():
    """Print welcome banner."""
    print("\n" + "="*80)
    print("IT Skills Advisor - Agentic RAG Chatbot")
    print("Multi-step reasoning | LLM refinement | Tool usage")
    print("="*80)


def get_student_level():
    """Get student level from user."""
    print("\nWhat's your current level?")
    print("1. Freshman")
    print("2. Sophomore")
    print("3. Junior")
    print("4. Senior")
    print("5. Graduate")
    
    choice = input("\nEnter choice (1-5, or press Enter for Junior): ").strip()
    
    levels = {
        '1': 'Freshman',
        '2': 'Sophomore',
        '3': 'Junior',
        '4': 'Senior',
        '5': 'Graduate'
    }
    
    return levels.get(choice, 'Junior')


def main():
    """Main agentic chatbot interface."""
    print_banner()
    
    try:
        # Get student level
        student_level = get_student_level()
        print(f"\n✓ Configured for {student_level} students.\n")
        
        # Initialize agentic RAG system
        print("Initializing Agentic RAG system...")
        bot = AgenticRAGChatbot()
        print("✓ System ready!\n")
        
        # Explain the agentic approach
        print("="*80)
        print("How Agentic RAG Works:")
        print("="*80)
        print("1. 🧠 Query Analysis - Understands your intent")
        print("2. 📋 Search Planning - Plans multi-step retrieval")
        print("3. 🔍 Semantic Search - Finds relevant data using AI")
        print("4. 💭 Reasoning - LLM analyzes and connects information")
        print("5. ✍️  Drafting - Creates initial response")
        print("6. ✨ Refinement - LLM improves clarity and accuracy")
        print("7. ✓  Verification - Quality check before delivery")
        print("="*80 + "\n")
        
        # Example questions
        print("Example questions:")
        print("  - What skills should I learn as a Junior?")
        print("  - Compare Python vs JavaScript for beginners")
        print("  - Show me the best GenAI resources")
        print("  - What's the career path for an AI engineer?")
        print("\nType 'quit' to exit.\n")
        
        # Chat loop
        while True:
            # Get user input
            user_message = input("You: ").strip()
            
            if not user_message:
                continue
            
            if user_message.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\nBot: Thanks for chatting! Keep learning! 🚀\n")
                break
            
            if user_message.lower() == 'level':
                student_level = get_student_level()
                print(f"\n✓ Updated to {student_level} level.\n")
                continue
            
            # Process with agentic RAG
            try:
                response = bot.chat(user_message, student_level=student_level)
                print("\nBot:")
                print(response)
                print("\n" + "-"*80 + "\n")
            
            except Exception as e:
                print(f"\nBot: I encountered an error: {e}")
                print("Please try rephrasing your question.\n")
                import traceback
                traceback.print_exc()
    
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋\n")
    
    except Exception as e:
        print(f"\nError: {e}")
        print("\nPlease ensure:")
        print("1. Supabase is configured")
        print("2. Database schema is set up")
        print("3. Vector embeddings are enabled")
        print("4. Data is loaded")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()



