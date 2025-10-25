"""Content Scraper Agent for discovering GenAI learning resources."""

from typing import List, Dict, Any, TypedDict
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import config


class ContentState(TypedDict):
    """State for content scraper agent."""
    query: str
    raw_results: List[Dict[str, Any]]
    filtered_results: List[Dict[str, Any]]
    categorized_results: List[Dict[str, Any]]
    error: str


@tool
def search_web_content(query: str) -> List[Dict[str, Any]]:
    """Search the web for GenAI learning content using Tavily API or fallback methods.
    
    Args:
        query: Search query for GenAI learning content
        
    Returns:
        List of search results with metadata
    """
    results = []
    
    # Try Tavily API first if available
    if config.TAVILY_API_KEY:
        try:
            from tavily import TavilyClient
            client = TavilyClient(api_key=config.TAVILY_API_KEY)
            
            search_results = client.search(
                query=f"{query} GenAI generative AI tutorial course learning",
                max_results=config.MAX_SEARCH_RESULTS,
                search_depth="advanced"
            )
            
            for result in search_results.get('results', []):
                results.append({
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'description': result.get('content', ''),
                    'source': 'tavily',
                    'timestamp': datetime.now().isoformat()
                })
        except Exception as e:
            print(f"Tavily search failed: {e}, using fallback method")
    
    # Fallback: Use Google search simulation with common learning platforms
    if not results:
        learning_platforms = [
            f"https://www.coursera.org/search?query={query}%20generative%20AI",
            f"https://www.udemy.com/courses/search/?q={query}%20GenAI",
            f"https://learn.microsoft.com/en-us/search/?terms={query}%20generative%20AI",
        ]
        
        for url in learning_platforms:
            try:
                platform_name = url.split('/')[2].replace('www.', '').split('.')[0]
                results.append({
                    'title': f"{query} courses on {platform_name.title()}",
                    'url': url,
                    'description': f"Search results for {query} related to GenAI on {platform_name}",
                    'source': platform_name,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception:
                continue
    
    # Add some curated GenAI resources
    curated_resources = [
        {
            'title': 'OpenAI Documentation',
            'url': 'https://platform.openai.com/docs',
            'description': 'Official OpenAI API documentation and guides for GenAI applications',
            'source': 'openai',
            'timestamp': datetime.now().isoformat()
        },
        {
            'title': 'LangChain Documentation',
            'url': 'https://python.langchain.com/docs/get_started/introduction',
            'description': 'Comprehensive guide to building GenAI applications with LangChain',
            'source': 'langchain',
            'timestamp': datetime.now().isoformat()
        },
        {
            'title': 'Hugging Face Courses',
            'url': 'https://huggingface.co/learn',
            'description': 'Free courses on NLP, transformers, and generative AI',
            'source': 'huggingface',
            'timestamp': datetime.now().isoformat()
        }
    ]
    
    results.extend(curated_resources)
    return results[:config.MAX_SEARCH_RESULTS]


@tool
def categorize_content(content_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Categorize learning content by type (tutorial, course, article, etc.).
    
    Args:
        content_list: List of content items to categorize
        
    Returns:
        Content list with category labels added
    """
    categorized = []
    
    for item in content_list:
        title = item.get('title', '').lower()
        url = item.get('url', '').lower()
        description = item.get('description', '').lower()
        
        # Simple keyword-based categorization
        if 'course' in title or 'coursera' in url or 'udemy' in url:
            category = 'course'
        elif 'tutorial' in title or 'guide' in title or 'how to' in title:
            category = 'tutorial'
        elif 'documentation' in title or 'docs' in url or 'api' in url:
            category = 'documentation'
        elif 'video' in title or 'youtube' in url:
            category = 'video'
        else:
            category = 'article'
        
        item['category'] = category
        item['relevance_score'] = calculate_relevance(item)
        categorized.append(item)
    
    # Sort by relevance score
    categorized.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
    return categorized


def calculate_relevance(item: Dict[str, Any]) -> float:
    """Calculate relevance score for a content item.
    
    Args:
        item: Content item with metadata
        
    Returns:
        Relevance score between 0 and 1
    """
    score = 0.5  # Base score
    
    genai_keywords = ['genai', 'generative ai', 'gpt', 'llm', 'langchain', 'openai', 'transformer']
    title = item.get('title', '').lower()
    description = item.get('description', '').lower()
    
    # Boost score for GenAI-specific keywords
    for keyword in genai_keywords:
        if keyword in title:
            score += 0.15
        if keyword in description:
            score += 0.05
    
    # Boost for trusted sources
    trusted_sources = ['openai', 'huggingface', 'microsoft', 'google', 'coursera']
    source = item.get('source', '').lower()
    if any(ts in source for ts in trusted_sources):
        score += 0.1
    
    return min(score, 1.0)


class ContentScraperAgent:
    """Agent for discovering and curating GenAI learning content."""
    
    def __init__(self):
        """Initialize the content scraper agent."""
        config.validate_config()
        self.llm = ChatOpenAI(
            model=config.LLM_MODEL,
            temperature=config.LLM_TEMPERATURE,
            api_key=config.OPENAI_API_KEY
        )
        self.tools = [search_web_content, categorize_content]
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the agent workflow graph."""
        workflow = StateGraph(ContentState)
        
        # Define nodes
        workflow.add_node("search", self._search_node)
        workflow.add_node("filter", self._filter_node)
        workflow.add_node("categorize", self._categorize_node)
        
        # Define edges
        workflow.set_entry_point("search")
        workflow.add_edge("search", "filter")
        workflow.add_edge("filter", "categorize")
        workflow.add_edge("categorize", END)
        
        return workflow.compile()
    
    def _search_node(self, state: ContentState) -> ContentState:
        """Execute web search for content."""
        try:
            results = search_web_content.invoke(state['query'])
            state['raw_results'] = results
        except Exception as e:
            state['error'] = f"Search failed: {str(e)}"
            state['raw_results'] = []
        
        return state
    
    def _filter_node(self, state: ContentState) -> ContentState:
        """Filter search results based on quality."""
        raw_results = state.get('raw_results', [])
        
        # Use LLM to assess quality
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a content quality assessor. Evaluate if the following content is suitable for learning GenAI."),
            ("user", "Content: {content}\nIs this high-quality learning content? Answer only 'yes' or 'no'.")
        ])
        
        filtered = []
        for item in raw_results:
            # Simple filtering based on presence of key information
            if item.get('title') and item.get('url') and item.get('description'):
                filtered.append(item)
        
        state['filtered_results'] = filtered
        return state
    
    def _categorize_node(self, state: ContentState) -> ContentState:
        """Categorize and score filtered content."""
        filtered_results = state.get('filtered_results', [])
        
        try:
            categorized = categorize_content.invoke(filtered_results)
            state['categorized_results'] = categorized
        except Exception as e:
            state['error'] = f"Categorization failed: {str(e)}"
            # Ensure fallback results have required fields
            for item in filtered_results:
                if 'category' not in item:
                    item['category'] = 'article'
                if 'relevance_score' not in item:
                    item['relevance_score'] = calculate_relevance(item)
            state['categorized_results'] = filtered_results
        
        return state
    
    def run(self, query: str) -> List[Dict[str, Any]]:
        """Run the content scraper agent.
        
        Args:
            query: Search query for learning content
            
        Returns:
            List of categorized learning resources
        """
        initial_state = ContentState(
            query=query,
            raw_results=[],
            filtered_results=[],
            categorized_results=[],
            error=""
        )
        
        result = self.graph.invoke(initial_state)
        return result.get('categorized_results', [])

