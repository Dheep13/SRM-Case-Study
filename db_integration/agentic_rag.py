"""Agentic RAG system with LLM-driven query planning and refinement."""

from typing import List, Dict, Any, TypedDict
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.tools import tool
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


@tool
def analyze_query(query: str, student_level: str) -> Dict[str, Any]:
    """Analyze user query to determine intent and required information.
    
    Args:
        query: User's question
        student_level: Student's current level
        
    Returns:
        Query analysis with intent, entities, and search strategy
    """
    llm = ChatOpenAI(model=config.LLM_MODEL, temperature=0.3)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a query analyzer for an IT skills database.
        Analyze the user's query and determine:
        1. Primary intent (skill_discovery, resource_finding, career_advice, comparison, trend_analysis)
        2. Key entities (skills, technologies, job roles mentioned)
        3. Search strategy (what data to retrieve)
        4. Student context relevance
        
        Return as JSON with: intent, entities, search_strategy, context_needs"""),
        ("user", "Query: {query}\nStudent Level: {level}")
    ])
    
    response = llm.invoke(prompt.format_messages(query=query, level=student_level))
    
    try:
        analysis = json.loads(response.content)
    except:
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
    
    query_embedding = embeddings.embed_query(query)
    
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
    except:
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
    
    query_embedding = embeddings.embed_query(query)
    
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
    except:
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
        """Build agentic RAG workflow graph."""
        workflow = StateGraph(AgenticRAGState)
        
        # Define nodes
        workflow.add_node("analyze", self._analyze_node)
        workflow.add_node("plan_search", self._plan_search_node)
        workflow.add_node("retrieve", self._retrieve_node)
        workflow.add_node("reason", self._reason_node)
        workflow.add_node("draft", self._draft_node)
        workflow.add_node("refine", self._refine_node)
        workflow.add_node("verify", self._verify_node)
        
        # Define edges
        workflow.set_entry_point("analyze")
        workflow.add_edge("analyze", "plan_search")
        workflow.add_edge("plan_search", "retrieve")
        workflow.add_edge("retrieve", "reason")
        workflow.add_edge("reason", "draft")
        workflow.add_edge("draft", "refine")
        workflow.add_edge("refine", "verify")
        
        # Conditional edge from verify
        workflow.add_conditional_edges(
            "verify",
            self._should_refine_again,
            {
                "refine_again": "reason",
                "done": END
            }
        )
        
        return workflow.compile()
    
    def _analyze_node(self, state: AgenticRAGState) -> AgenticRAGState:
        """Analyze user query to understand intent."""
        print("\n[Agent] Analyzing query...")
        
        analysis = analyze_query.invoke({
            "query": state['user_query'],
            "student_level": state['student_level']
        })
        
        state['query_analysis'] = analysis
        state['reasoning_steps'].append(f"Identified intent: {analysis.get('intent', 'unknown')}")
        
        print(f"  Intent: {analysis.get('intent')}")
        print(f"  Entities: {analysis.get('entities')}")
        
        return state
    
    def _plan_search_node(self, state: AgenticRAGState) -> AgenticRAGState:
        """Plan search queries based on analysis."""
        print("\n[Agent] Planning search strategy...")
        
        analysis = state['query_analysis']
        queries = []
        
        # Generate specific search queries based on intent
        if analysis.get('intent') == 'skill_discovery':
            queries.append(state['user_query'])
            queries.append(f"{state['student_level']} student skills")
        
        elif analysis.get('intent') == 'resource_finding':
            for entity in analysis.get('entities', []):
                queries.append(f"{entity} learning resources")
        
        elif analysis.get('intent') == 'comparison':
            queries.append(state['user_query'])
            for entity in analysis.get('entities', []):
                queries.append(entity)
        
        else:
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
        
        # Semantic search for skills
        for query in state['search_queries']:
            skills = semantic_search_skills.invoke({"query": query, "limit": 5})
            retrieved['skills'].extend(skills)
        
        # Remove duplicates
        seen_skills = set()
        unique_skills = []
        for skill in retrieved['skills']:
            skill_id = skill.get('skill_id') or skill.get('id')
            if skill_id not in seen_skills:
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
        
        state['retrieved_data'] = retrieved
        state['reasoning_steps'].append(
            f"Retrieved {len(retrieved['skills'])} skills, "
            f"{len(retrieved['resources'])} resources"
        )
        
        print(f"  Found {len(retrieved['skills'])} relevant skills")
        print(f"  Found {len(retrieved['resources'])} relevant resources")
        
        return state
    
    def _reason_node(self, state: AgenticRAGState) -> AgenticRAGState:
        """Reason about retrieved data and form insights."""
        print("\n[Agent] Reasoning about data...")
        
        # Use LLM to reason about the data
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert reasoning agent. Analyze the retrieved data 
            and form insights to answer the user's query. Consider:
            1. What are the most relevant pieces of information?
            2. How do they relate to each other?
            3. What conclusions can be drawn?
            4. What additional context is needed?
            
            Return reasoning as structured thoughts."""),
            ("user", """Query: {query}
            Student Level: {level}
            Intent: {intent}
            
            Retrieved Skills: {skills}
            Retrieved Resources: {resources}
            Recommendations: {recommendations}
            
            Provide reasoning steps to answer this query:""")
        ])
        
        retrieved = state['retrieved_data']
        response = self.llm.invoke(prompt.format_messages(
            query=state['user_query'],
            level=state['student_level'],
            intent=state['query_analysis'].get('intent', 'unknown'),
            skills=json.dumps([s.get('skill_name', 'Unknown') for s in retrieved['skills'][:5]]),
            resources=json.dumps([r.get('title', 'Unknown') for r in retrieved['resources'][:3]]),
            recommendations=json.dumps([r.get('skill_name', 'Unknown') for r in retrieved['recommendations'][:3]])
        ))
        
        reasoning = response.content
        state['reasoning_steps'].append(f"Reasoning: {reasoning[:100]}...")
        
        print(f"  Generated reasoning insights")
        
        return state
    
    def _draft_node(self, state: AgenticRAGState) -> AgenticRAGState:
        """Draft initial response."""
        print("\n[Agent] Drafting response...")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an IT Skills Advisor. Create a helpful, actionable response
            based on the analysis and retrieved data. Be specific, include actual skill names,
            demand scores, and resource links. Format with markdown."""),
            ("user", """User Query: {query}
            Student Level: {level}
            
            Analysis: {analysis}
            Reasoning: {reasoning}
            
            Retrieved Data:
            Skills: {skills}
            Resources: {resources}
            Recommendations: {recommendations}
            
            Draft a comprehensive response:""")
        ])
        
        retrieved = state['retrieved_data']
        response = self.llm.invoke(prompt.format_messages(
            query=state['user_query'],
            level=state['student_level'],
            analysis=json.dumps(state['query_analysis']),
            reasoning="\n".join(state['reasoning_steps']),
            skills=json.dumps(retrieved['skills'][:5], indent=2),
            resources=json.dumps(retrieved['resources'][:3], indent=2),
            recommendations=json.dumps(retrieved['recommendations'][:3], indent=2)
        ))
        
        state['draft_response'] = response.content
        
        print(f"  Created draft response ({len(response.content)} chars)")
        
        return state
    
    def _refine_node(self, state: AgenticRAGState) -> AgenticRAGState:
        """Refine and improve the response."""
        print("\n[Agent] Refining response...")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a response refinement expert. Improve the draft response by:
            1. Making it more concise and clear
            2. Ensuring all claims are backed by data
            3. Adding specific next steps
            4. Improving formatting and readability
            5. Checking accuracy of demand scores and URLs
            
            Keep the helpful tone but make it more polished."""),
            ("user", """Original Query: {query}
            Student Level: {level}
            
            Draft Response:
            {draft}
            
            Refine this response:""")
        ])
        
        response = self.llm.invoke(prompt.format_messages(
            query=state['user_query'],
            level=state['student_level'],
            draft=state['draft_response']
        ))
        
        state['refined_response'] = response.content
        
        print(f"  Refined response")
        
        return state
    
    def _verify_node(self, state: AgenticRAGState) -> AgenticRAGState:
        """Verify response quality and completeness."""
        print("\n[Agent] Verifying response quality...")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a quality verifier. Check if the response:
            1. Fully answers the user's query
            2. Is accurate based on the data
            3. Is appropriate for the student level
            4. Provides actionable advice
            
            Score from 0-1 and note if refinement is needed."""),
            ("user", """Query: {query}
            Response: {response}
            
            Rate quality (0-1):""")
        ])
        
        response = self.llm.invoke(prompt.format_messages(
            query=state['user_query'],
            response=state['refined_response'][:500]
        ))
        
        try:
            # Extract score (simple parsing)
            content = response.content.lower()
            if '0.9' in content or '0.8' in content or 'excellent' in content:
                score = 0.9
            elif '0.7' in content or 'good' in content:
                score = 0.7
            else:
                score = 0.6
        except:
            score = 0.7
        
        state['confidence_score'] = score
        state['needs_clarification'] = score < 0.7
        
        print(f"  Quality score: {score:.2f}")
        
        return state
    
    def _should_refine_again(self, state: AgenticRAGState) -> str:
        """Decide if response needs another refinement."""
        # Only refine once more if quality is too low
        if state['confidence_score'] < 0.6 and len(state['reasoning_steps']) < 10:
            return "refine_again"
        return "done"
    
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
            needs_clarification=False
        )
        
        result = self.graph.invoke(initial_state)
        
        print("\n" + "="*80)
        print(f"Processing Complete (Confidence: {result['confidence_score']:.2f})")
        print("="*80 + "\n")
        
        return result['refined_response']



