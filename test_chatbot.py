"""Simplified chatbot for debugging."""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import config
import json

class SimpleChatbot:
    """Simplified chatbot without LangGraph."""
    
    def __init__(self):
        """Initialize simple chatbot."""
        self.llm = ChatOpenAI(
            model=config.LLM_MODEL,
            temperature=0.7,
            api_key=config.OPENAI_API_KEY
        )
    
    def chat(self, user_query: str, student_level: str = "Junior") -> str:
        """Simple chat without complex workflow."""
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", f"""You are a helpful AI assistant for IT students at the {student_level} level.
                Provide helpful, accurate responses about programming, technology, and career advice.
                Keep responses concise and appropriate for the student's level."""),
                ("user", "{query}")
            ])
            
            response = self.llm.invoke(prompt.format_messages(query=user_query))
            return response.content
            
        except Exception as e:
            return f"Error: {str(e)}"

# Test function
def test_simple_chatbot():
    """Test the simplified chatbot."""
    try:
        print("Creating simple chatbot...")
        bot = SimpleChatbot()
        print("Chatbot created successfully")
        
        print("Testing chat...")
        response = bot.chat("What is Python?", "Junior")
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_simple_chatbot()
