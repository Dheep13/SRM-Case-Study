"""Tech News Fetcher using Tavily API for real-time technology news with date support."""

from typing import List, Dict, Any
from datetime import datetime, timedelta
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def fetch_tech_news(query: str = "AI technology", max_results: int = 10, days_back: int = 7) -> List[Dict[str, Any]]:
    """Fetch latest tech news using Tavily API with date filtering.
    
    Args:
        query: Search query for tech news (default: "AI technology")
        max_results: Maximum number of news articles to return
        days_back: How many days back to search (default: 7 days)
        
    Returns:
        List of news articles with metadata and dates
    """
    news_articles = []
    
    # Check if Tavily API key is available
    if not config.TAVILY_API_KEY:
        print("Warning: TAVILY_API_KEY not set, returning empty news list")
        return news_articles
    
    try:
        from tavily import TavilyClient
        
        client = TavilyClient(api_key=config.TAVILY_API_KEY)
        
        # Add time-based keywords to get recent news
        time_query = f"{query} news latest recent"
        
        # Search for recent tech news
        search_results = client.search(
            query=time_query,
            search_depth="basic",
            max_results=max_results * 2,  # Get more to filter by date
            include_domains=["techcrunch.com", "theverge.com", "wired.com", "arstechnica.com", 
                           "venturebeat.com", "zdnet.com", "engadget.com", "thenextweb.com",
                           "microsoft.com/blog", "blog.google", "openai.com/blog", "mit.edu",
                           "reuters.com/technology", "bloomberg.com/technology"]
        )
        
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        if search_results and 'results' in search_results:
            for idx, result in enumerate(search_results['results']):
                # Determine category based on content
                content_lower = (result.get('content', '') + result.get('title', '')).lower()
                category = categorize_tech_news(content_lower)
                
                # Determine relevance based on source and recency
                url = result.get('url', '')
                relevance = determine_relevance(url, content_lower)
                
                # Try to extract/estimate publish date
                published_date, time_ago = estimate_publish_date(result, url)
                
                # Filter by date if we can determine it
                # If we can't determine date, include it anyway (better to show than miss)
                if published_date and published_date < cutoff_date:
                    continue  # Skip old articles
                
                # Extract source from URL
                source = extract_source_name(url)
                
                news_articles.append({
                    'id': idx + 1,
                    'title': result.get('title', 'Untitled'),
                    'summary': result.get('content', 'No summary available')[:250],  # Limit summary length
                    'url': url,
                    'category': category,
                    'published': time_ago,
                    'published_date': published_date.isoformat() if published_date else None,
                    'source': source,
                    'relevance': relevance,
                    'score': result.get('score', 0.5),
                    'fetched_at': datetime.now().isoformat()
                })
                
                # Stop once we have enough
                if len(news_articles) >= max_results:
                    break
        
    except Exception as e:
        print(f"Error fetching tech news from Tavily: {e}")
        import traceback
        traceback.print_exc()
    
    # Sort by date (most recent first) if we have dates
    news_articles.sort(key=lambda x: x.get('published_date') or '0', reverse=True)
    
    return news_articles[:max_results]


def estimate_publish_date(result: Dict[str, Any], url: str) -> tuple:
    """Estimate publish date from article metadata or URL.
    
    Args:
        result: Search result from Tavily
        url: Article URL
        
    Returns:
        Tuple of (datetime object or None, human-readable time string)
    """
    now = datetime.now()
    
    # Try to extract date from URL patterns
    # Common patterns: /2024/11/08/, /20241108/, etc.
    import re
    
    # Pattern: /YYYY/MM/DD/ or /YYYY-MM-DD/
    date_pattern = r'/(\d{4})[/-](\d{1,2})[/-](\d{1,2})/'
    match = re.search(date_pattern, url)
    if match:
        try:
            year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
            article_date = datetime(year, month, day)
            time_ago = format_time_ago(article_date)
            return article_date, time_ago
        except:
            pass
    
    # Pattern: /YYYYMMDD/
    date_pattern2 = r'/(\d{8})/'
    match = re.search(date_pattern2, url)
    if match:
        try:
            date_str = match.group(1)
            article_date = datetime.strptime(date_str, '%Y%m%d')
            time_ago = format_time_ago(article_date)
            return article_date, time_ago
        except:
            pass
    
    # Check if Tavily provided a published_date field
    if 'published_date' in result:
        try:
            article_date = datetime.fromisoformat(result['published_date'].replace('Z', '+00:00'))
            time_ago = format_time_ago(article_date)
            return article_date, time_ago
        except:
            pass
    
    # Estimate based on search recency (Tavily returns recent results first)
    # Assume within last few days
    estimated_date = now - timedelta(hours=12)  # Assume ~12 hours old on average
    return estimated_date, "Recently"


def format_time_ago(article_date: datetime) -> str:
    """Format datetime as human-readable time ago.
    
    Args:
        article_date: Publication datetime
        
    Returns:
        Human-readable string like "2 hours ago"
    """
    now = datetime.now()
    diff = now - article_date
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "Just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 604800:  # Less than a week
        days = int(seconds / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"
    elif seconds < 2592000:  # Less than a month
        weeks = int(seconds / 604800)
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    else:
        return article_date.strftime("%b %d, %Y")


def categorize_tech_news(content: str) -> str:
    """Categorize tech news based on content keywords."""
    if any(keyword in content for keyword in ['ai', 'artificial intelligence', 'machine learning', 'deep learning', 'gpt', 'llm', 'generative']):
        return 'AI/ML'
    elif any(keyword in content for keyword in ['education', 'learning', 'student', 'course', 'university', 'school']):
        return 'Education'
    elif any(keyword in content for keyword in ['programming', 'developer', 'code', 'software', 'framework', 'library', 'python', 'javascript']):
        return 'Development'
    elif any(keyword in content for keyword in ['security', 'cybersecurity', 'hack', 'vulnerability', 'breach', 'encryption']):
        return 'Security'
    elif any(keyword in content for keyword in ['quantum', 'quantum computing']):
        return 'Quantum'
    elif any(keyword in content for keyword in ['cloud', 'aws', 'azure', 'google cloud', 'serverless']):
        return 'Cloud'
    elif any(keyword in content for keyword in ['blockchain', 'crypto', 'web3', 'nft']):
        return 'Blockchain'
    elif any(keyword in content for keyword in ['mobile', 'ios', 'android', 'app']):
        return 'Mobile'
    else:
        return 'Technology'


def determine_relevance(url: str, content: str) -> str:
    """Determine relevance level based on source and keywords."""
    # High relevance sources
    high_relevance_domains = ['techcrunch.com', 'theverge.com', 'wired.com', 'arstechnica.com',
                             'openai.com', 'microsoft.com', 'blog.google', 'mit.edu', 'reuters.com', 'bloomberg.com']
    
    # Check if from high-relevance source
    if any(domain in url for domain in high_relevance_domains):
        return 'high'
    
    # Check for important keywords in content
    important_keywords = ['breakthrough', 'launch', 'release', 'announce', 'unveil', 'revolutionary', 
                         'major', 'significant', 'important', 'critical', 'new']
    
    if any(keyword in content for keyword in important_keywords):
        return 'high'
    
    # Check for educational/practical keywords
    practical_keywords = ['tutorial', 'guide', 'how to', 'learn', 'course', 'tips']
    
    if any(keyword in content for keyword in practical_keywords):
        return 'medium'
    
    return 'medium'  # Default to medium


def extract_source_name(url: str) -> str:
    """Extract readable source name from URL."""
    source_map = {
        'techcrunch.com': 'TechCrunch',
        'theverge.com': 'The Verge',
        'wired.com': 'Wired',
        'arstechnica.com': 'Ars Technica',
        'venturebeat.com': 'VentureBeat',
        'zdnet.com': 'ZDNet',
        'engadget.com': 'Engadget',
        'thenextweb.com': 'The Next Web',
        'microsoft.com': 'Microsoft',
        'blog.google': 'Google',
        'openai.com': 'OpenAI',
        'mit.edu': 'MIT Technology Review',
        'reuters.com': 'Reuters',
        'bloomberg.com': 'Bloomberg'
    }
    
    for domain, name in source_map.items():
        if domain in url:
            return name
    
    # Extract domain name as fallback
    try:
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        domain = domain.replace('www.', '').replace('.com', '').replace('.org', '').replace('.net', '')
        return domain.title()
    except:
        return 'Tech News'


if __name__ == "__main__":
    """Test the tech news fetcher."""
    print("Fetching latest tech news from the past 7 days...")
    news = fetch_tech_news("AI artificial intelligence programming", max_results=5, days_back=7)
    
    print(f"\nFound {len(news)} recent news articles:\n")
    for article in news:
        print(f"📰 {article['title']}")
        print(f"   🕒 {article['published']} | Source: {article['source']} | Category: {article['category']}")
        print(f"   Relevance: {article['relevance'].upper()}")
        print(f"   Summary: {article['summary'][:100]}...")
        print(f"   URL: {article['url']}\n")

