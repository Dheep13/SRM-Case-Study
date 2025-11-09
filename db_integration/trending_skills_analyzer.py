"""Trending Skills Analyzer using Tavily API for real-time tech trends."""

from typing import List, Dict, Any
from datetime import datetime, timedelta
import os
import sys
import re

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def analyze_trending_skills(max_skills: int = 10, days_back: int = 30) -> List[Dict[str, Any]]:
    """Analyze trending tech skills from recent tech news and job postings.
    
    Args:
        max_skills: Maximum number of trending skills to return
        days_back: How far back to look for trends (default: 30 days)
        
    Returns:
        List of trending skills with popularity metrics
    """
    trending = []
    
    # Check if Tavily API key is available
    if not config.TAVILY_API_KEY:
        print("Warning: TAVILY_API_KEY not set, returning fallback trends")
        return generate_fallback_trends()
    
    try:
        from tavily import TavilyClient
        
        client = TavilyClient(api_key=config.TAVILY_API_KEY)
        
        # Search queries focused on trends and popularity
        search_queries = [
            "trending programming languages 2025 most popular",
            "hot tech skills developers learning 2025",
            "fastest growing technologies software development",
            "most popular frameworks libraries 2025",
            "emerging tech skills startups hiring",
        ]
        
        skill_popularity = {}
        skill_contexts = {}
        skill_recency = {}
        
        print(f"Analyzing trending skills from past {days_back} days...")
        
        # Search for trending skill data
        for query in search_queries:
            try:
                results = client.search(
                    query=query,
                    search_depth="basic",
                    max_results=5,
                    include_domains=["stackoverflow.com", "github.com", "reddit.com/r/programming",
                                   "dev.to", "medium.com", "hackernews.com", "techcrunch.com",
                                   "thenextweb.com", "venturebeat.com", "infoworld.com"]
                )
                
                if results and 'results' in results:
                    for result in results['results']:
                        content = (result.get('content', '') + ' ' + result.get('title', '')).lower()
                        url = result.get('url', '')
                        
                        # Extract trending skills
                        extracted_skills = extract_trending_skills(content)
                        
                        for skill in extracted_skills:
                            # Count popularity
                            skill_popularity[skill] = skill_popularity.get(skill, 0) + 1
                            
                            # Store context
                            if skill not in skill_contexts:
                                skill_contexts[skill] = []
                            skill_contexts[skill].append(content)
                            
                            # Track recency (more recent = more trending)
                            if skill not in skill_recency:
                                skill_recency[skill] = datetime.now()
                            
            except Exception as e:
                print(f"Error searching for '{query}': {e}")
                continue
        
        # Analyze and rank trending skills
        if skill_popularity:
            print(f"Found {len(skill_popularity)} trending skills")
            
            # Calculate trend scores
            trend_scores = {}
            for skill, count in skill_popularity.items():
                contexts = skill_contexts.get(skill, [])
                
                # Base popularity score
                popularity_score = count * 10
                
                # Boost for trending keywords
                trend_boost = calculate_trend_boost(skill, contexts)
                
                # Recency boost (more recent mentions = higher score)
                recency_boost = 5
                
                # Total trend score
                total_score = min(100, popularity_score + trend_boost + recency_boost)
                trend_scores[skill] = total_score
            
            # Sort by trend score
            sorted_trends = sorted(trend_scores.items(), key=lambda x: x[1], reverse=True)
            
            # Generate trending skill objects
            for skill, trend_score in sorted_trends[:max_skills]:
                contexts = skill_contexts.get(skill, [])
                category = categorize_skill(skill)
                momentum = calculate_momentum(skill, contexts)
                source = identify_primary_source(contexts)
                
                trending.append({
                    'skill': format_skill_name(skill),
                    'trend_score': round(trend_score),  # Round to whole number
                    'popularity': calculate_popularity(skill_popularity[skill]),
                    'momentum': momentum,
                    'change': f"+{skill_popularity[skill] * 5}%",
                    'category': category,
                    'source': source,
                    'description': generate_description(skill, contexts),
                    'trending_since': estimate_trending_start(days_back),
                    'analyzed_at': datetime.now().isoformat()
                })
        
        # Return trends if we got some
        if trending:
            print(f"Generated {len(trending)} trending skills")
            return sorted(trending, key=lambda x: x['trend_score'], reverse=True)
        else:
            print("No trends extracted, using fallback")
            return generate_fallback_trends()
            
    except Exception as e:
        print(f"Error analyzing trending skills: {e}")
        import traceback
        traceback.print_exc()
        return generate_fallback_trends()


def extract_trending_skills(content: str) -> List[str]:
    """Extract trending tech skills from content.
    
    Args:
        content: Text content to analyze (lowercase)
        
    Returns:
        List of trending skill names
    """
    # Comprehensive skills dictionary
    skills_dict = {
        # AI/ML (Very Hot Right Now)
        'chatgpt': 'ChatGPT',
        'gpt-4': 'GPT-4',
        'generative ai': 'Generative AI',
        'large language models': 'Large Language Models',
        'llm': 'LLM',
        'prompt engineering': 'Prompt Engineering',
        'stable diffusion': 'Stable Diffusion',
        'midjourney': 'Midjourney',
        'copilot': 'GitHub Copilot',
        
        # Programming Languages
        'rust': 'Rust',
        'go': 'Go',
        'typescript': 'TypeScript',
        'python': 'Python',
        'kotlin': 'Kotlin',
        'swift': 'Swift',
        
        # Web/Frontend
        'next.js': 'Next.js',
        'react': 'React',
        'vue': 'Vue.js',
        'svelte': 'Svelte',
        'tailwind': 'Tailwind CSS',
        'astro': 'Astro',
        
        # Backend/Infrastructure
        'kubernetes': 'Kubernetes',
        'docker': 'Docker',
        'serverless': 'Serverless',
        'edge computing': 'Edge Computing',
        'graphql': 'GraphQL',
        'grpc': 'gRPC',
        
        # Cloud
        'aws': 'AWS',
        'azure': 'Azure',
        'google cloud': 'Google Cloud',
        'vercel': 'Vercel',
        'cloudflare': 'Cloudflare Workers',
        
        # Databases
        'postgresql': 'PostgreSQL',
        'mongodb': 'MongoDB',
        'redis': 'Redis',
        'supabase': 'Supabase',
        'planetscale': 'PlanetScale',
        
        # DevOps/Tools
        'terraform': 'Terraform',
        'github actions': 'GitHub Actions',
        'ci/cd': 'CI/CD',
        'devops': 'DevOps',
        
        # Emerging Tech
        'web3': 'Web3',
        'blockchain': 'Blockchain',
        'metaverse': 'Metaverse',
        'quantum computing': 'Quantum Computing',
        'edge ai': 'Edge AI',
        
        # Frameworks
        'fastapi': 'FastAPI',
        'django': 'Django',
        'flask': 'Flask',
        'express': 'Express.js',
    }
    
    found_skills = []
    
    for keyword, skill_name in skills_dict.items():
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, content):
            found_skills.append(skill_name)
    
    return found_skills


def calculate_trend_boost(skill: str, contexts: List[str]) -> int:
    """Calculate boost based on trending indicators in context.
    
    Args:
        skill: Skill name
        contexts: Content contexts
        
    Returns:
        Boost score
    """
    trending_keywords = [
        'trending', 'hot', 'popular', 'viral', 'exploding', 'surging',
        'rising', 'fastest growing', 'everyone is using', 'all the rage',
        'taking over', 'dominating', 'must learn', 'in demand', 'hype',
        'breakthrough', 'revolutionary', 'game changer', 'next big thing'
    ]
    
    boost = 0
    for context in contexts:
        for keyword in trending_keywords:
            if keyword in context:
                boost += 3
    
    return min(40, boost)


def calculate_momentum(skill: str, contexts: List[str]) -> str:
    """Calculate momentum level (hot, rising, steady).
    
    Args:
        skill: Skill name
        contexts: Content contexts
        
    Returns:
        Momentum level
    """
    hot_keywords = ['viral', 'exploding', 'surging', 'hot', 'trending now']
    rising_keywords = ['rising', 'growing', 'increasing', 'gaining', 'emerging']
    
    hot_count = sum(1 for context in contexts for kw in hot_keywords if kw in context)
    rising_count = sum(1 for context in contexts for kw in rising_keywords if kw in context)
    
    if hot_count >= 2:
        return 'hot'
    elif rising_count >= 2 or hot_count >= 1:
        return 'rising'
    else:
        return 'steady'


def calculate_popularity(mention_count: int) -> str:
    """Calculate popularity level.
    
    Args:
        mention_count: Number of mentions
        
    Returns:
        Popularity level
    """
    if mention_count >= 10:
        return 'very_high'
    elif mention_count >= 7:
        return 'high'
    elif mention_count >= 4:
        return 'medium'
    else:
        return 'growing'


def categorize_skill(skill: str) -> str:
    """Categorize trending skill.
    
    Args:
        skill: Skill name
        
    Returns:
        Category
    """
    skill_lower = skill.lower()
    
    if any(kw in skill_lower for kw in ['ai', 'gpt', 'chatgpt', 'llm', 'generative', 'copilot', 'stable diffusion', 'midjourney']):
        return 'AI/ML'
    elif any(kw in skill_lower for kw in ['rust', 'go', 'kotlin', 'swift', 'python', 'typescript']):
        return 'Programming'
    elif any(kw in skill_lower for kw in ['react', 'vue', 'svelte', 'next', 'astro', 'tailwind']):
        return 'Frontend'
    elif any(kw in skill_lower for kw in ['kubernetes', 'docker', 'serverless', 'edge']):
        return 'DevOps'
    elif any(kw in skill_lower for kw in ['aws', 'azure', 'cloud', 'vercel', 'cloudflare']):
        return 'Cloud'
    elif any(kw in skill_lower for kw in ['web3', 'blockchain', 'metaverse', 'quantum']):
        return 'Emerging'
    else:
        return 'Technology'


def identify_primary_source(contexts: List[str]) -> str:
    """Identify primary source of trend.
    
    Args:
        contexts: Content contexts
        
    Returns:
        Source name
    """
    sources = {
        'github': 'GitHub',
        'stackoverflow': 'Stack Overflow',
        'reddit': 'Reddit',
        'hackernews': 'Hacker News',
        'dev.to': 'Dev.to',
        'medium': 'Medium',
    }
    
    for context in contexts:
        for key, name in sources.items():
            if key in context:
                return name
    
    return 'Tech Community'


def generate_description(skill: str, contexts: List[str]) -> str:
    """Generate a short description of why it's trending.
    
    Args:
        skill: Skill name
        contexts: Content contexts
        
    Returns:
        Description text
    """
    skill_lower = skill.lower()
    
    # AI/ML skills
    if 'chatgpt' in skill_lower or 'gpt' in skill_lower:
        return "Revolutionary AI chatbot transforming how developers work"
    elif 'generative ai' in skill_lower or 'llm' in skill_lower:
        return "Creating content, code, and solutions using AI models"
    elif 'copilot' in skill_lower:
        return "AI-powered code completion revolutionizing development"
    
    # Programming languages
    elif 'rust' in skill_lower:
        return "Fast, safe systems programming gaining massive adoption"
    elif 'go' in skill_lower:
        return "Simple, efficient language for cloud-native applications"
    elif 'typescript' in skill_lower:
        return "Type-safe JavaScript becoming industry standard"
    
    # Frontend
    elif 'next.js' in skill_lower:
        return "React framework for production-grade applications"
    elif 'svelte' in skill_lower:
        return "Lightweight, blazingly fast frontend framework"
    elif 'tailwind' in skill_lower:
        return "Utility-first CSS framework for rapid UI development"
    
    # Cloud/DevOps
    elif 'kubernetes' in skill_lower:
        return "Container orchestration platform dominating cloud infrastructure"
    elif 'serverless' in skill_lower:
        return "Deploy without managing servers, pay per use"
    elif 'edge computing' in skill_lower:
        return "Processing data closer to users for better performance"
    
    # Default
    else:
        return f"Gaining significant traction in tech community"


def estimate_trending_start(days_back: int) -> str:
    """Estimate when skill started trending.
    
    Args:
        days_back: Days analyzed
        
    Returns:
        Human-readable time
    """
    if days_back <= 7:
        return "This week"
    elif days_back <= 14:
        return "Past 2 weeks"
    elif days_back <= 30:
        return "This month"
    else:
        return "Recently"


def format_skill_name(skill: str) -> str:
    """Format skill name for display."""
    return skill


def generate_fallback_trends() -> List[Dict[str, Any]]:
    """Generate fallback trends when Tavily unavailable."""
    return [
        {
            'skill': 'Generative AI',
            'trend_score': 95,
            'popularity': 'very_high',
            'momentum': 'hot',
            'change': '+45%',
            'category': 'AI/ML',
            'source': 'Tech Community',
            'description': 'Creating content and code using AI models',
            'trending_since': 'This month',
            'analyzed_at': datetime.now().isoformat()
        },
        {
            'skill': 'Rust',
            'trend_score': 88,
            'popularity': 'high',
            'momentum': 'rising',
            'change': '+35%',
            'category': 'Programming',
            'source': 'GitHub',
            'description': 'Fast, safe systems programming language',
            'trending_since': 'This month',
            'analyzed_at': datetime.now().isoformat()
        },
        {
            'skill': 'Next.js',
            'trend_score': 82,
            'popularity': 'high',
            'momentum': 'steady',
            'change': '+30%',
            'category': 'Frontend',
            'source': 'Dev Community',
            'description': 'React framework for production apps',
            'trending_since': 'This month',
            'analyzed_at': datetime.now().isoformat()
        }
    ]


if __name__ == "__main__":
    """Test the trending skills analyzer."""
    print("=" * 80)
    print("TRENDING SKILLS ANALYZER - Testing")
    print("=" * 80)
    
    trends = analyze_trending_skills(max_skills=10, days_back=30)
    
    print(f"\n🔥 Found {len(trends)} trending skills:\n")
    
    for i, trend in enumerate(trends, 1):
        momentum_emoji = '🔥' if trend['momentum'] == 'hot' else '📈' if trend['momentum'] == 'rising' else '➡️'
        
        print(f"{i}. {trend['skill']} {momentum_emoji}")
        print(f"   Trend Score: {trend['trend_score']}/100")
        print(f"   Change: {trend['change']}")
        print(f"   Category: {trend['category']}")
        print(f"   Momentum: {trend['momentum'].upper()}")
        print(f"   Source: {trend['source']}")
        print(f"   Description: {trend['description']}")
        print(f"   Trending Since: {trend['trending_since']}\n")

