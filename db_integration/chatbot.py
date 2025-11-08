"""Chatbot interface for querying IT skills database using natural language."""

from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from db_integration.supabase_client import SupabaseManager
import config
import json


class SkillsChatbot:
    """Chatbot for querying IT skills and learning resources database."""
    
    def __init__(self, session_id: Optional[str] = None):
        """Initialize the chatbot.
        
        Args:
            session_id: Optional session ID for conversation tracking
        """
        self.db = SupabaseManager()
        self.llm = ChatOpenAI(
            model=config.LLM_MODEL,
            temperature=0.7,
            api_key=config.OPENAI_API_KEY
        )
        self.embeddings = OpenAIEmbeddings(api_key=config.OPENAI_API_KEY)
        self.session_id = session_id or str(uuid.uuid4())
        self.conversation_history = []
        
        # System prompt for the chatbot
        self.system_prompt = """You are an IT Skills Advisor chatbot for college students. 
You have access to a database of IT skills, learning resources, and industry trends.

Your role is to:
- Help students discover what skills they should learn
- Recommend learning resources for specific skills
- Explain skill demand and trends
- Provide personalized learning paths based on student level
- Answer questions about IT careers and technologies

Be friendly, concise, and actionable. Always provide specific skill names and resource links when relevant.

When students ask about skills, consider:
- Their current level (Freshman, Sophomore, Junior, Senior, Graduate)
- Skill difficulty (Beginner, Intermediate, Advanced)
- Current demand scores (0-100)
- Available learning resources

Format your responses with:
- Clear bullet points for lists
- Specific skill names in bold
- Resource links when available
- Demand scores when discussing popularity
"""
    
    def create_embedding(self, text: str) -> List[float]:
        """Create embedding for text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        return self.embeddings.embed_query(text)
    
    def search_relevant_context(self, query: str) -> Dict[str, Any]:
        """Search database for relevant context.
        
        Args:
            query: User query
            
        Returns:
            Relevant context from database
        """
        context = {
            'skills': [],
            'resources': [],
            'stats': {}
        }
        
        # Get embedding for query
        query_embedding = self.create_embedding(query)
        
        # Search for similar skills using embedding
        try:
            result = self.db.client.rpc(
                'search_similar_skills',
                {
                    'query_embedding': query_embedding,
                    'match_threshold': 0.6,
                    'match_count': 5
                }
            ).execute()
            context['skills'] = result.data if result.data else []
        except:
            # Fallback to text search
            skills = self.db.get_top_skills(limit=10)
            query_lower = query.lower()
            context['skills'] = [
                s for s in skills 
                if query_lower in s.get('skill_name', '').lower() or 
                   query_lower in s.get('category', '').lower()
            ][:5]
        
        # Search for similar resources
        try:
            result = self.db.client.rpc(
                'search_similar_resources',
                {
                    'query_embedding': query_embedding,
                    'match_threshold': 0.6,
                    'match_count': 3
                }
            ).execute()
            context['resources'] = result.data if result.data else []
        except:
            # Fallback to getting all resources
            all_resources = self.db.get_all_resources(limit=20)
            query_lower = query.lower()
            context['resources'] = [
                r for r in all_resources
                if query_lower in r.get('title', '').lower() or
                   query_lower in r.get('description', '').lower()
            ][:3]
        
        # Get general stats
        try:
            top_skills = self.db.get_top_skills_for_students(limit=5)
            context['stats'] = {
                'top_skills': [s.get('skill_name') for s in top_skills[:5]],
                'total_skills': len(self.db.get_top_skills(limit=100))
            }
        except:
            pass
        
        return context
    
    def format_context_for_llm(self, context: Dict[str, Any]) -> str:
        """Format context for LLM.
        
        Args:
            context: Context dictionary
            
        Returns:
            Formatted context string
        """
        formatted = "Database Context:\n\n"
        
        # Format skills
        if context['skills']:
            formatted += "Relevant Skills:\n"
            for skill in context['skills']:
                formatted += f"- {skill.get('skill_name', 'Unknown')} "
                formatted += f"(Category: {skill.get('category', 'N/A')}, "
                formatted += f"Difficulty: {skill.get('difficulty_level', 'N/A')}, "
                formatted += f"Demand: {skill.get('demand_score', 0)})\n"
            formatted += "\n"
        
        # Format resources
        if context['resources']:
            formatted += "Learning Resources:\n"
            for resource in context['resources']:
                formatted += f"- {resource.get('title', 'Unknown')}\n"
                formatted += f"  URL: {resource.get('url', 'N/A')}\n"
                formatted += f"  Category: {resource.get('category', 'N/A')}\n"
            formatted += "\n"
        
        # Format stats
        if context['stats']:
            formatted += "Database Stats:\n"
            formatted += f"- Total skills tracked: {context['stats'].get('total_skills', 0)}\n"
            if context['stats'].get('top_skills'):
                formatted += f"- Top 5 skills: {', '.join(context['stats']['top_skills'])}\n"
        
        return formatted
    
    def chat(self, user_message: str, student_level: str = "Junior") -> str:
        """Send a message to the chatbot.
        
        Args:
            user_message: User's message
            student_level: Student's current level
            
        Returns:
            Bot's response
        """
        # Search for relevant context
        context = self.search_relevant_context(user_message)
        formatted_context = self.format_context_for_llm(context)
        
        # Create messages
        messages = [
            SystemMessage(content=self.system_prompt),
            SystemMessage(content=f"Student Level: {student_level}"),
            SystemMessage(content=formatted_context)
        ]
        
        # Add conversation history
        messages.extend(self.conversation_history[-6:])  # Last 3 exchanges
        
        # Add current message
        messages.append(HumanMessage(content=user_message))
        
        # Get response
        response = self.llm.invoke(messages)
        bot_response = response.content
        
        # Update conversation history
        self.conversation_history.append(HumanMessage(content=user_message))
        self.conversation_history.append(AIMessage(content=bot_response))
        
        # Save to database
        try:
            self.db.client.table('chat_history').insert({
                'session_id': self.session_id,
                'user_message': user_message,
                'bot_response': bot_response,
                'context_used': json.dumps(context)
            }).execute()
        except:
            pass  # Don't fail if chat history save fails
        
        return bot_response
    
    def get_skill_details(self, skill_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific skill.
        
        Args:
            skill_name: Name of the skill
            
        Returns:
            Skill details with resources
        """
        try:
            result = self.db.client.rpc(
                'get_skill_with_resources',
                {'skill_name_param': skill_name}
            ).execute()
            
            if result.data:
                # Group by skill
                skill_data = {
                    'skill_name': result.data[0]['skill_name'],
                    'category': result.data[0]['category'],
                    'demand_score': result.data[0]['demand_score'],
                    'resources': []
                }
                
                for row in result.data:
                    if row['resource_title']:
                        skill_data['resources'].append({
                            'title': row['resource_title'],
                            'url': row['resource_url'],
                            'category': row['resource_category']
                        })
                
                return skill_data
        except:
            pass
        
        return {}
    
    def get_recommendations(self, student_level: str, focus_area: str = None) -> List[Dict[str, Any]]:
        """Get skill recommendations for student.
        
        Args:
            student_level: Student's current level
            focus_area: Optional focus area
            
        Returns:
            List of recommended skills
        """
        try:
            result = self.db.client.rpc(
                'get_recommended_skills_for_query',
                {
                    'student_level_param': student_level,
                    'focus_area_param': focus_area
                }
            ).execute()
            
            return result.data if result.data else []
        except:
            # Fallback
            return self.db.get_top_skills_for_students(limit=10)
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
    
    def get_session_history(self) -> List[Dict[str, Any]]:
        """Get chat history for current session.
        
        Returns:
            List of chat messages
        """
        try:
            result = self.db.client.table('chat_history')\
                .select('*')\
                .eq('session_id', self.session_id)\
                .order('created_at', desc=False)\
                .execute()
            
            return result.data if result.data else []
        except:
            return []



