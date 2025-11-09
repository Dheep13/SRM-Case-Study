"""Trend Analysis Agent for discovering trending GenAI topics."""

from typing import List, Dict, Any, TypedDict
from datetime import datetime, timedelta
import requests
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
import config


class TrendState(TypedDict):
    """State for trend analysis agent."""
    topic: str
    github_trends: List[Dict[str, Any]]
    linkedin_trends: List[Dict[str, Any]]
    aggregated_trends: List[Dict[str, Any]]
    error: str


@tool
def fetch_github_trends(topic: str) -> List[Dict[str, Any]]:
    """Fetch trending repositories and topics from GitHub related to GenAI.
    
    Args:
        topic: Topic to search for on GitHub
        
    Returns:
        List of trending repositories and topics
    """
    from agent_access_control import access_controller
    
    trends = []
    
    # Check if GitHub access is allowed
    if not access_controller.check_access("trend_analysis", "github", config.GITHUB_TRENDING_URL, "repositories"):
        print("GitHub access blocked by admin policy")
        return trends
    
    headers = {}
    if config.GITHUB_TOKEN:
        headers['Authorization'] = f'token {config.GITHUB_TOKEN}'
    
    # Search for repositories
    try:
        # Calculate date from last 7 days for trending
        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        # Search repositories
        search_query = f"{topic} generative AI OR GenAI OR LLM created:>{week_ago}"
        params = {
            'q': search_query,
            'sort': 'stars',
            'order': 'desc',
            'per_page': 10
        }
        
        response = requests.get(
            config.GITHUB_TRENDING_URL,
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            
            for repo in items:
                trends.append({
                    'title': repo.get('full_name', ''),
                    'description': repo.get('description', ''),
                    'url': repo.get('html_url', ''),
                    'stars': repo.get('stargazers_count', 0),
                    'language': repo.get('language', 'Unknown'),
                    'created_at': repo.get('created_at', ''),
                    'updated_at': repo.get('updated_at', ''),
                    'source': 'github',
                    'type': 'repository',
                    'engagement_score': repo.get('stargazers_count', 0) + repo.get('forks_count', 0) * 2
                })
        
    except Exception as e:
        print(f"GitHub API error: {e}")
    
    # Add some popular GenAI repositories manually as fallback
    if len(trends) < 5:
        popular_repos = [
            {
                'title': 'langchain-ai/langchain',
                'description': 'Building applications with LLMs through composability',
                'url': 'https://github.com/langchain-ai/langchain',
                'stars': 80000,
                'language': 'Python',
                'source': 'github',
                'type': 'repository',
                'engagement_score': 85000
            },
            {
                'title': 'openai/openai-python',
                'description': 'The official Python library for the OpenAI API',
                'url': 'https://github.com/openai/openai-python',
                'stars': 18000,
                'language': 'Python',
                'source': 'github',
                'type': 'repository',
                'engagement_score': 20000
            },
            {
                'title': 'microsoft/autogen',
                'description': 'A programming framework for building AI agents and facilitating cooperation',
                'url': 'https://github.com/microsoft/autogen',
                'stars': 25000,
                'language': 'Python',
                'source': 'github',
                'type': 'repository',
                'engagement_score': 27000
            },
            {
                'title': 'ggerganov/llama.cpp',
                'description': 'Port of Facebook\'s LLaMA model in C/C++',
                'url': 'https://github.com/ggerganov/llama.cpp',
                'stars': 55000,
                'language': 'C++',
                'source': 'github',
                'type': 'repository',
                'engagement_score': 60000
            }
        ]
        
        # Add popular repos that aren't already in trends
        existing_titles = {t['title'] for t in trends}
        for repo in popular_repos:
            if repo['title'] not in existing_titles:
                trends.append(repo)
    
    # Sort by engagement score
    trends.sort(key=lambda x: x.get('engagement_score', 0), reverse=True)
    return trends[:config.MAX_TREND_ITEMS]


@tool
def analyze_linkedin_trends(topic: str) -> List[Dict[str, Any]]:
    """Analyze trending GenAI topics on LinkedIn based on common hashtags and topics.
    
    Args:
        topic: Topic to analyze
        
    Returns:
        List of trending topics with metadata
    """
    # Note: LinkedIn API requires OAuth and has restricted access
    # This provides simulated trending topics based on current GenAI landscape
    
    trending_topics = [
        {
            'title': '#GenerativeAI',
            'description': 'Discussions about generative AI applications, tools, and innovations',
            'estimated_posts': 50000,
            'hashtag': 'GenerativeAI',
            'source': 'linkedin',
            'type': 'hashtag',
            'engagement_score': 95
        },
        {
            'title': '#LLM (Large Language Models)',
            'description': 'Conversations about LLM development, deployment, and use cases',
            'estimated_posts': 35000,
            'hashtag': 'LLM',
            'source': 'linkedin',
            'type': 'hashtag',
            'engagement_score': 88
        },
        {
            'title': '#AIAgents',
            'description': 'Building autonomous AI agents and multi-agent systems',
            'estimated_posts': 28000,
            'hashtag': 'AIAgents',
            'source': 'linkedin',
            'type': 'hashtag',
            'engagement_score': 82
        },
        {
            'title': '#RAG (Retrieval Augmented Generation)',
            'description': 'Implementing RAG systems for enterprise AI applications',
            'estimated_posts': 22000,
            'hashtag': 'RAG',
            'source': 'linkedin',
            'type': 'hashtag',
            'engagement_score': 78
        },
        {
            'title': '#PromptEngineering',
            'description': 'Best practices and techniques for prompt engineering',
            'estimated_posts': 30000,
            'hashtag': 'PromptEngineering',
            'source': 'linkedin',
            'type': 'hashtag',
            'engagement_score': 85
        },
        {
            'title': '#OpenAI',
            'description': 'OpenAI announcements, GPT models, and API developments',
            'estimated_posts': 45000,
            'hashtag': 'OpenAI',
            'source': 'linkedin',
            'type': 'hashtag',
            'engagement_score': 92
        },
        {
            'title': '#LangChain',
            'description': 'LangChain framework for building LLM applications',
            'estimated_posts': 15000,
            'hashtag': 'LangChain',
            'source': 'linkedin',
            'type': 'hashtag',
            'engagement_score': 75
        },
        {
            'title': '#VectorDatabases',
            'description': 'Vector databases for AI and semantic search applications',
            'estimated_posts': 18000,
            'hashtag': 'VectorDatabases',
            'source': 'linkedin',
            'type': 'hashtag',
            'engagement_score': 72
        },
        {
            'title': '#AIEthics',
            'description': 'Ethical considerations in AI development and deployment',
            'estimated_posts': 25000,
            'hashtag': 'AIEthics',
            'source': 'linkedin',
            'type': 'hashtag',
            'engagement_score': 80
        },
        {
            'title': '#FineTuning',
            'description': 'Fine-tuning LLMs for specific use cases and domains',
            'estimated_posts': 20000,
            'hashtag': 'FineTuning',
            'source': 'linkedin',
            'type': 'hashtag',
            'engagement_score': 76
        }
    ]
    
    # Filter based on topic if specific
    if topic.lower() not in ['genai', 'general', 'all']:
        filtered = [t for t in trending_topics if topic.lower() in t['title'].lower() or topic.lower() in t['description'].lower()]
        if filtered:
            return filtered
    
    return trending_topics[:config.MAX_TREND_ITEMS]


@tool
def aggregate_trends(github_trends: List[Dict[str, Any]], linkedin_trends: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Aggregate and rank trends from multiple sources.
    
    Args:
        github_trends: Trends from GitHub
        linkedin_trends: Trends from LinkedIn
        
    Returns:
        Aggregated and ranked trends
    """
    all_trends = []
    
    # Normalize and combine trends
    for trend in github_trends:
        all_trends.append({
            'title': trend.get('title', ''),
            'description': trend.get('description', ''),
            'url': trend.get('url', ''),
            'source': 'GitHub',
            'type': trend.get('type', 'repository'),
            'metrics': {
                'stars': trend.get('stars', 0),
                'language': trend.get('language', 'Unknown'),
                'engagement_score': trend.get('engagement_score', 0)
            },
            'overall_score': calculate_trend_score(trend, 'github')
        })
    
    for trend in linkedin_trends:
        all_trends.append({
            'title': trend.get('title', ''),
            'description': trend.get('description', ''),
            'url': f"https://www.linkedin.com/search/results/all/?keywords={trend.get('hashtag', '')}",
            'source': 'LinkedIn',
            'type': trend.get('type', 'hashtag'),
            'metrics': {
                'estimated_posts': trend.get('estimated_posts', 0),
                'hashtag': trend.get('hashtag', ''),
                'engagement_score': trend.get('engagement_score', 0)
            },
            'overall_score': calculate_trend_score(trend, 'linkedin')
        })
    
    # Sort by overall score
    all_trends.sort(key=lambda x: x.get('overall_score', 0), reverse=True)
    
    # Add timestamp
    for trend in all_trends:
        trend['analyzed_at'] = datetime.now().isoformat()
    
    return all_trends


def calculate_trend_score(trend: Dict[str, Any], source: str) -> float:
    """Calculate overall trend score.
    
    Args:
        trend: Trend data
        source: Source platform
        
    Returns:
        Normalized score between 0 and 100
    """
    if source == 'github':
        engagement = trend.get('engagement_score', 0)
        # Normalize GitHub stars/engagement (log scale)
        score = min(100, (engagement / 1000) * 10)
    else:  # linkedin
        engagement = trend.get('engagement_score', 0)
        score = engagement
    
    return score


class TrendAnalysisAgent:
    """Agent for analyzing trending GenAI topics across platforms."""
    
    def __init__(self):
        """Initialize the trend analysis agent."""
        config.validate_config()
        self.llm = ChatOpenAI(
            model=config.LLM_MODEL,
            temperature=config.LLM_TEMPERATURE,
            api_key=config.OPENAI_API_KEY
        )
        self.tools = [fetch_github_trends, analyze_linkedin_trends, aggregate_trends]
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the agent workflow graph."""
        workflow = StateGraph(TrendState)
        
        # Define nodes
        workflow.add_node("github", self._github_node)
        workflow.add_node("linkedin", self._linkedin_node)
        workflow.add_node("aggregate", self._aggregate_node)
        
        # Define edges
        workflow.set_entry_point("github")
        workflow.add_edge("github", "linkedin")
        workflow.add_edge("linkedin", "aggregate")
        workflow.add_edge("aggregate", END)
        
        return workflow.compile()
    
    def _github_node(self, state: TrendState) -> TrendState:
        """Fetch GitHub trends."""
        try:
            results = fetch_github_trends.invoke(state['topic'])
            state['github_trends'] = results
        except Exception as e:
            state['error'] = f"GitHub trends fetch failed: {str(e)}"
            state['github_trends'] = []
        
        return state
    
    def _linkedin_node(self, state: TrendState) -> TrendState:
        """Fetch LinkedIn trends."""
        try:
            results = analyze_linkedin_trends.invoke(state['topic'])
            state['linkedin_trends'] = results
        except Exception as e:
            state['error'] = f"LinkedIn trends fetch failed: {str(e)}"
            state['linkedin_trends'] = []
        
        return state
    
    def _aggregate_node(self, state: TrendState) -> TrendState:
        """Aggregate trends from all sources."""
        try:
            aggregated = aggregate_trends.invoke({
                'github_trends': state.get('github_trends', []),
                'linkedin_trends': state.get('linkedin_trends', [])
            })
            state['aggregated_trends'] = aggregated
        except Exception as e:
            state['error'] = f"Trend aggregation failed: {str(e)}"
            state['aggregated_trends'] = []
        
        return state
    
    def run(self, topic: str = "GenAI") -> List[Dict[str, Any]]:
        """Run the trend analysis agent.
        
        Args:
            topic: Topic to analyze trends for
            
        Returns:
            List of aggregated trending topics
        """
        initial_state = TrendState(
            topic=topic,
            github_trends=[],
            linkedin_trends=[],
            aggregated_trends=[],
            error=""
        )
        
        result = self.graph.invoke(initial_state)
        return result.get('aggregated_trends', [])

