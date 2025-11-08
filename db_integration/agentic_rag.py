"""Agentic RAG system with LLM-driven query planning and refinement - FIXED VERSION."""

from typing import List, Dict, Any, TypedDict
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from db_integration.supabase_client import SupabaseManager
import config
import json


class AgenticRAGState(TypedDict):
    """State for agentic RAG workflow."""
    user_query: str
    student_level: str
    query_analysis: Dict[str, Any]
    search_queries: List[str]
    retrieved_data: Dict[str, Any]
    reasoning_steps: List[str]
    draft_response: str
    refined_response: str
    confidence_score: float
    needs_clarification: bool
    refinement_count: int  # Track refinement iterations


@tool
def analyze_query(query: str, student_level: str) -> Dict[str, Any]:
    """Analyze user query to determine intent and required information.

    Args:
        query: User's question
        student_level: Student's current level

    Returns:
        Query analysis with intent, entities, and search strategy
    """
    # Use faster, cheaper model for simple analysis
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, max_tokens=200)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """Analyze query intent. Return ONLY valid JSON with no markdown formatting: {"intent": "<skill_discovery|resource_finding|career_advice|comparison|trend_analysis>", "entities": ["<skills/tech>"], "context_needs": ["skills"]}"""),
        ("user", "Query: {query}\nLevel: {level}")
    ])

    try:
        response = llm.invoke(prompt.format_messages(query=query, level=student_level))
        
        # Clean response content - remove markdown code blocks if present
        content = response.content.strip()
        if content.startswith("```json"):
            content = content[7:]  # Remove ```json
        if content.startswith("```"):
            content = content[3:]  # Remove ```
        if content.endswith("```"):
            content = content[:-3]  # Remove trailing ```
        content = content.strip()
        
        analysis = json.loads(content)
        
        # Validate required fields
        if 'intent' not in analysis:
            analysis['intent'] = 'skill_discovery'
        if 'entities' not in analysis:
            analysis['entities'] = []
        if 'context_needs' not in analysis:
            analysis['context_needs'] = ['skills', 'resources']
            
    except Exception as e:
        print(f"Warning: Failed to parse query analysis: {e}")
        # Fallback parsing
        analysis = {
            "intent": "skill_discovery",
            "entities": [],
            "search_strategy": "broad_search",
            "context_needs": ["skills", "resources"]
        }

    return analysis


@tool
def semantic_search_skills(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Search for relevant skills using semantic search.
    
    Args:
        query: Search query
        limit: Number of results
        
    Returns:
        List of relevant skills
    """
    db = SupabaseManager()
    embeddings = OpenAIEmbeddings(api_key=config.OPENAI_API_KEY)
    
    try:
        query_embedding = embeddings.embed_query(query)
    except Exception as e:
        print(f"Warning: Embedding failed ({e}), using fallback")
        return db.get_top_skills(limit=limit)
    
    try:
        result = db.client.rpc(
            'search_similar_skills',
            {
                'query_embedding': query_embedding,
                'match_threshold': 0.6,
                'match_count': limit
            }
        ).execute()
        
        return result.data if result.data else []
    except Exception as e:
        print(f"Warning: Database search failed ({e}), using fallback")
        # Fallback to top skills
        return db.get_top_skills(limit=limit)


@tool
def semantic_search_resources(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Search for relevant learning resources using semantic search.
    
    Args:
        query: Search query
        limit: Number of results
        
    Returns:
        List of relevant resources
    """
    db = SupabaseManager()
    embeddings = OpenAIEmbeddings(api_key=config.OPENAI_API_KEY)
    
    try:
        query_embedding = embeddings.embed_query(query)
    except Exception as e:
        print(f"Warning: Embedding failed ({e}), using fallback")
        return db.get_all_resources(limit=limit)
    
    try:
        result = db.client.rpc(
            'search_similar_resources',
            {
                'query_embedding': query_embedding,
                'match_threshold': 0.6,
                'match_count': limit
            }
        ).execute()
        
        return result.data if result.data else []
    except Exception as e:
        print(f"Warning: Database search failed ({e}), using fallback")
        return db.get_all_resources(limit=limit)


@tool
def get_skill_details(skill_name: str) -> Dict[str, Any]:
    """Get detailed information about a specific skill.
    
    Args:
        skill_name: Name of the skill
        
    Returns:
        Detailed skill information with resources
    """
    db = SupabaseManager()
    
    try:
        result = db.client.rpc(
            'get_skill_with_resources',
            {'skill_name_param': skill_name}
        ).execute()
        
        if result.data:
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


@tool
def get_recommendations_for_level(student_level: str, focus_area: str = None) -> List[Dict[str, Any]]:
    """Get personalized skill recommendations for student level.
    
    Args:
        student_level: Student's current level
        focus_area: Optional focus area
        
    Returns:
        List of recommended skills
    """
    db = SupabaseManager()
    
    try:
        result = db.client.rpc(
            'get_recommended_skills_for_query',
            {
                'student_level_param': student_level,
                'focus_area_param': focus_area
            }
        ).execute()
        
        return result.data if result.data else []
    except:
        return db.get_top_skills_for_students(limit=10)


class AgenticRAGChatbot:
    """Agentic RAG chatbot with multi-step reasoning and refinement."""
    
    def __init__(self):
        """Initialize agentic RAG system."""
        self.db = SupabaseManager()
        self.llm = ChatOpenAI(
            model=config.LLM_MODEL,
            temperature=0.7,
            api_key=config.OPENAI_API_KEY
        )
        self.tools = [
            analyze_query,
            semantic_search_skills,
            semantic_search_resources,
            get_skill_details,
            get_recommendations_for_level
        ]
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build optimized agentic RAG workflow graph."""
        workflow = StateGraph(AgenticRAGState)

        # Define nodes - OPTIMIZED: Reduced from 7 to 4 nodes
        workflow.add_node("analyze", self._analyze_node)
        workflow.add_node("plan_search", self._plan_search_node)
        workflow.add_node("retrieve", self._retrieve_node)
        workflow.add_node("generate", self._generate_response_node)  # Combined reason+draft+refine

        # Define edges - Simplified linear flow
        workflow.set_entry_point("analyze")
        workflow.add_edge("analyze", "plan_search")
        workflow.add_edge("plan_search", "retrieve")
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)

        return workflow.compile()
    
    def _analyze_node(self, state: AgenticRAGState) -> AgenticRAGState:
        """Analyze user query to understand intent."""
        print("\n[Agent] Analyzing query...")
        
        try:
            analysis = analyze_query.invoke({
                "query": state['user_query'],
                "student_level": state['student_level']
            })
            
            state['query_analysis'] = analysis
            state['reasoning_steps'].append(f"Identified intent: {analysis.get('intent', 'unknown')}")
            
            print(f"  Intent: {analysis.get('intent')}")
            print(f"  Entities: {analysis.get('entities')}")
        except Exception as e:
            print(f"  Error in analysis: {e}")
            state['query_analysis'] = {
                "intent": "skill_discovery",
                "entities": [],
                "context_needs": ["skills", "resources"]
            }
            state['reasoning_steps'].append(f"Analysis failed, using default intent")
        
        return state
    
    def _plan_search_node(self, state: AgenticRAGState) -> AgenticRAGState:
        """Plan search queries based on analysis."""
        print("\n[Agent] Planning search strategy...")
        
        analysis = state.get('query_analysis', {})
        queries = []
        
        # Generate specific search queries based on intent
        intent = analysis.get('intent', 'skill_discovery')
        
        if intent == 'skill_discovery':
            queries.append(state['user_query'])
            queries.append(f"{state['student_level']} student skills")
        
        elif intent == 'resource_finding':
            for entity in analysis.get('entities', []):
                queries.append(f"{entity} learning resources")
        
        elif intent == 'comparison':
            queries.append(state['user_query'])
            for entity in analysis.get('entities', []):
                queries.append(entity)
        
        else:
            queries.append(state['user_query'])
        
        # Ensure we have at least one query
        if not queries:
            queries.append(state['user_query'])
        
        state['search_queries'] = queries
        state['reasoning_steps'].append(f"Planned {len(queries)} search queries")
        
        print(f"  Search queries: {queries}")
        
        return state
    
    def _retrieve_node(self, state: AgenticRAGState) -> AgenticRAGState:
        """Retrieve relevant data from database."""
        print("\n[Agent] Retrieving data...")
        
        retrieved = {
            'skills': [],
            'resources': [],
            'recommendations': []
        }
        
        try:
            # Semantic search for skills
            for query in state.get('search_queries', [state['user_query']]):
                skills = semantic_search_skills.invoke({"query": query, "limit": 5})
                retrieved['skills'].extend(skills)
            
            # Remove duplicates
            seen_skills = set()
            unique_skills = []
            for skill in retrieved['skills']:
                skill_id = skill.get('skill_id') or skill.get('id')
                if skill_id and skill_id not in seen_skills:
                    seen_skills.add(skill_id)
                    unique_skills.append(skill)
            retrieved['skills'] = unique_skills[:10]
            
            # Get resources
            resources = semantic_search_resources.invoke({
                "query": state['user_query'],
                "limit": 5
            })
            retrieved['resources'] = resources
            
            # Get recommendations for student level
            recs = get_recommendations_for_level.invoke({
                "student_level": state['student_level']
            })
            retrieved['recommendations'] = recs[:5]
            
        except Exception as e:
            print(f"  Error retrieving data: {e}")
            import traceback
            traceback.print_exc()
        
        state['retrieved_data'] = retrieved
        state['reasoning_steps'].append(
            f"Retrieved {len(retrieved['skills'])} skills, "
            f"{len(retrieved['resources'])} resources"
        )
        
        print(f"  Found {len(retrieved['skills'])} relevant skills")
        print(f"  Found {len(retrieved['resources'])} relevant resources")
        
        return state
    
    def _generate_response_node(self, state: AgenticRAGState) -> AgenticRAGState:
        """OPTIMIZED: Generate complete response in one LLM call (combines reason+draft+refine)."""
        print("\n[Agent] Generating response...")

        try:
            # Single optimized prompt that does reasoning + drafting in one pass
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are an expert IT Skills Advisor. Based on the user's query and retrieved data:
1. Identify key insights from the data
2. Create a clear, actionable response with specific skills, demand scores, and resources
3. Format with markdown for readability
4. Tailor advice to the student's level

Be concise, specific, and helpful."""),
                ("user", """Query: {query}
Student Level: {level}
Intent: {intent}

Retrieved Skills (top 5):
{skills}

Resources:
{resources}

Recommendations:
{recommendations}

Generate a complete, polished response:""")
            ])

            retrieved = state.get('retrieved_data', {})
            query_analysis = state.get('query_analysis', {})

            # Format data concisely for faster processing
            skills_summary = "\n".join([
                f"- {s.get('skill_name', 'Unknown')} (Demand: {s.get('demand_score', 'N/A')})"
                for s in retrieved.get('skills', [])[:5]
            ])

            resources_summary = "\n".join([
                f"- {r.get('title', 'Unknown')}: {r.get('url', 'N/A')}"
                for r in retrieved.get('resources', [])[:3]
            ])

            recommendations_summary = "\n".join([
                f"- {r.get('skill_name', 'Unknown')}"
                for r in retrieved.get('recommendations', [])[:3]
            ])

            # Get intent safely with fallback
            intent = query_analysis.get('intent', 'general_inquiry') if isinstance(query_analysis, dict) else 'general_inquiry'

            response = self.llm.invoke(prompt.format_messages(
                query=state['user_query'],
                level=state['student_level'],
                intent=intent,
                skills=skills_summary or "No specific skills found",
                resources=resources_summary or "No resources found",
                recommendations=recommendations_summary or "No recommendations available"
            ))

            state['refined_response'] = response.content
            state['draft_response'] = response.content  # Keep for compatibility
            state['confidence_score'] = 0.9  # Assume high quality from optimized prompt
            state['reasoning_steps'].append("Generated complete response in single pass")

            print(f"  Generated response ({len(response.content)} chars)")

        except Exception as e:
            print(f"  Error generating response: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Provide fallback response
            state['refined_response'] = "I apologize, but I encountered an error while processing your request. Please try rephrasing your question or contact support if the issue persists."
            state['draft_response'] = state['refined_response']
            state['confidence_score'] = 0.3
            state['reasoning_steps'].append(f"Error during generation: {str(e)}")

        return state
    
    def chat(self, user_query: str, student_level: str = "Junior") -> str:
        """Process user query through agentic RAG workflow.
        
        Args:
            user_query: User's question
            student_level: Student's current level
            
        Returns:
            Refined response
        """
        print("\n" + "="*80)
        print("Agentic RAG Processing")
        print("="*80)
        
        try:
            initial_state = AgenticRAGState(
                user_query=user_query,
                student_level=student_level,
                query_analysis={},
                search_queries=[],
                retrieved_data={},
                reasoning_steps=[],
                draft_response="",
                refined_response="",
                confidence_score=0.0,
                needs_clarification=False,
                refinement_count=0  # Initialize counter
            )
            
            result = self.graph.invoke(initial_state)
            
            print("\n" + "="*80)
            print(f"Processing Complete (Confidence: {result['confidence_score']:.2f})")
            print("="*80 + "\n")
            
            return result['refined_response']
            
        except Exception as e:
            print(f"\nError in chat processing: {e}")
            import traceback
            traceback.print_exc()
            return f"I apologize, but I encountered an error while processing your request: {str(e)}"