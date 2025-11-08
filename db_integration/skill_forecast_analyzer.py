"""Skill Forecast Analyzer using Tavily API for real job market and tech trend data."""

from typing import List, Dict, Any
from datetime import datetime
import os
import sys
import re

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def analyze_skill_forecast(max_skills: int = 10) -> List[Dict[str, Any]]:
    """Analyze tech skills forecast using real job market and trend data from Tavily.
    
    Args:
        max_skills: Maximum number of skills to return
        
    Returns:
        List of skill forecasts with demand metrics
    """
    forecasts = []
    
    # Check if Tavily API key is available
    if not config.TAVILY_API_KEY:
        print("Warning: TAVILY_API_KEY not set, returning mock forecasts")
        return generate_fallback_forecasts()
    
    try:
        from tavily import TavilyClient
        
        client = TavilyClient(api_key=config.TAVILY_API_KEY)
        
        # Search queries for different skill categories
        search_queries = [
            "most in-demand tech skills 2025 job market AI machine learning",
            "highest paying programming languages 2025 developer skills",
            "emerging technology skills cloud computing cybersecurity",
            "software development trends 2025 job requirements",
        ]
        
        skill_mentions = {}
        skill_contexts = {}
        
        print("Analyzing skill demand from job market data...")
        
        # Search for skill demand data
        for query in search_queries:
            try:
                results = client.search(
                    query=query,
                    search_depth="basic",
                    max_results=5,
                    include_domains=["linkedin.com/jobs", "indeed.com", "stackoverflow.com",
                                   "github.com", "techcrunch.com", "zdnet.com",
                                   "forbes.com/technology", "dice.com"]
                )
                
                if results and 'results' in results:
                    for result in results['results']:
                        content = (result.get('content', '') + ' ' + result.get('title', '')).lower()
                        
                        # Extract and count skill mentions
                        extracted_skills = extract_skills_from_content(content)
                        
                        for skill in extracted_skills:
                            skill_mentions[skill] = skill_mentions.get(skill, 0) + 1
                            
                            # Store context for sentiment analysis
                            if skill not in skill_contexts:
                                skill_contexts[skill] = []
                            skill_contexts[skill].append(content)
                            
            except Exception as e:
                print(f"Error searching for '{query}': {e}")
                continue
        
        # Analyze and rank skills
        if skill_mentions:
            print(f"Found {len(skill_mentions)} unique skills mentioned")
            
            # Sort by mention count
            sorted_skills = sorted(skill_mentions.items(), key=lambda x: x[1], reverse=True)
            
            # Generate forecasts for top skills
            for skill, mention_count in sorted_skills[:max_skills]:
                # Analyze growth trend and demand
                contexts = skill_contexts.get(skill, [])
                growth_rate = calculate_growth_rate(skill, contexts, mention_count)
                demand_level = calculate_demand_level(mention_count, len(search_queries) * 5)
                category = categorize_skill(skill)
                
                forecasts.append({
                    'skill': format_skill_name(skill),
                    'current_demand': round(demand_level),  # Round to whole number
                    'forecast_demand': round(min(100, demand_level + growth_rate)),  # Round to whole number
                    'growth_rate': f"+{growth_rate}%",
                    'trend': 'up' if growth_rate > 0 else 'stable',
                    'category': category,
                    'confidence': calculate_confidence(mention_count),
                    'source': 'Job Market Analysis',
                    'analyzed_at': datetime.now().isoformat()
                })
        
        # If we got some forecasts, return them
        if forecasts:
            print(f"Generated {len(forecasts)} skill forecasts")
            return sorted(forecasts, key=lambda x: x['forecast_demand'], reverse=True)
        else:
            print("No skills extracted, using fallback")
            return generate_fallback_forecasts()
            
    except Exception as e:
        print(f"Error analyzing skill forecasts: {e}")
        import traceback
        traceback.print_exc()
        return generate_fallback_forecasts()


def extract_skills_from_content(content: str) -> List[str]:
    """Extract tech skills mentioned in content.
    
    Args:
        content: Text content to analyze (lowercase)
        
    Returns:
        List of skill names found
    """
    # Comprehensive list of tech skills to look for
    skills_dictionary = {
        # AI/ML
        'python': 'Python',
        'machine learning': 'Machine Learning',
        'artificial intelligence': 'Artificial Intelligence',
        'deep learning': 'Deep Learning',
        'tensorflow': 'TensorFlow',
        'pytorch': 'PyTorch',
        'data science': 'Data Science',
        'nlp': 'Natural Language Processing',
        'computer vision': 'Computer Vision',
        'generative ai': 'Generative AI',
        
        # Web Development
        'javascript': 'JavaScript',
        'typescript': 'TypeScript',
        'react': 'React',
        'node.js': 'Node.js',
        'angular': 'Angular',
        'vue': 'Vue.js',
        'html': 'HTML',
        'css': 'CSS',
        'web development': 'Web Development',
        
        # Backend
        'java': 'Java',
        'c++': 'C++',
        'go': 'Go',
        'rust': 'Rust',
        'php': 'PHP',
        'ruby': 'Ruby',
        '.net': '.NET',
        'c#': 'C#',
        
        # Cloud
        'aws': 'AWS',
        'azure': 'Azure',
        'google cloud': 'Google Cloud',
        'cloud computing': 'Cloud Computing',
        'docker': 'Docker',
        'kubernetes': 'Kubernetes',
        'devops': 'DevOps',
        'terraform': 'Terraform',
        
        # Database
        'sql': 'SQL',
        'postgresql': 'PostgreSQL',
        'mongodb': 'MongoDB',
        'redis': 'Redis',
        'database': 'Database Management',
        
        # Security
        'cybersecurity': 'Cybersecurity',
        'security': 'Information Security',
        'penetration testing': 'Penetration Testing',
        'ethical hacking': 'Ethical Hacking',
        
        # Mobile
        'mobile development': 'Mobile Development',
        'ios': 'iOS Development',
        'android': 'Android Development',
        'flutter': 'Flutter',
        'react native': 'React Native',
        
        # Other
        'git': 'Git',
        'agile': 'Agile',
        'api': 'API Development',
        'microservices': 'Microservices',
        'blockchain': 'Blockchain',
    }
    
    found_skills = []
    
    for skill_keyword, skill_name in skills_dictionary.items():
        # Use word boundaries for better matching
        pattern = r'\b' + re.escape(skill_keyword) + r'\b'
        if re.search(pattern, content):
            found_skills.append(skill_name)
    
    return found_skills


def calculate_growth_rate(skill: str, contexts: List[str], mention_count: int) -> int:
    """Calculate projected growth rate for a skill.
    
    Args:
        skill: Skill name
        contexts: Content contexts where skill was mentioned
        mention_count: Number of times mentioned
        
    Returns:
        Growth rate percentage
    """
    # Base growth on mention frequency
    base_growth = min(30, mention_count * 3)
    
    # Analyze sentiment in contexts
    growth_keywords = ['growing', 'emerging', 'high demand', 'increasing', 'trending',
                      'popular', 'essential', 'critical', 'hot', 'boom', 'rise',
                      'future', 'next generation', 'cutting edge', 'revolutionary']
    
    sentiment_boost = 0
    for context in contexts:
        for keyword in growth_keywords:
            if keyword in context:
                sentiment_boost += 2
    
    total_growth = min(50, base_growth + sentiment_boost)
    return total_growth


def calculate_demand_level(mention_count: int, total_results: int) -> int:
    """Calculate current demand level (0-100).
    
    Args:
        mention_count: Times skill was mentioned
        total_results: Total search results analyzed
        
    Returns:
        Demand level score
    """
    # Calculate percentage of results mentioning the skill
    percentage = (mention_count / max(total_results, 1)) * 100
    
    # Scale to 0-100 with reasonable thresholds
    if percentage >= 50:
        return 90
    elif percentage >= 30:
        return 75
    elif percentage >= 20:
        return 65
    elif percentage >= 10:
        return 55
    else:
        return max(30, int(percentage * 3))


def categorize_skill(skill: str) -> str:
    """Categorize skill by domain.
    
    Args:
        skill: Skill name
        
    Returns:
        Category name
    """
    skill_lower = skill.lower()
    
    if any(kw in skill_lower for kw in ['ai', 'machine learning', 'deep learning', 'data science', 'nlp', 'computer vision']):
        return 'AI/ML'
    elif any(kw in skill_lower for kw in ['javascript', 'react', 'angular', 'vue', 'web', 'html', 'css', 'frontend']):
        return 'Web Development'
    elif any(kw in skill_lower for kw in ['aws', 'azure', 'cloud', 'docker', 'kubernetes', 'devops']):
        return 'Cloud/DevOps'
    elif any(kw in skill_lower for kw in ['security', 'cybersecurity', 'hacking', 'penetration']):
        return 'Security'
    elif any(kw in skill_lower for kw in ['mobile', 'ios', 'android', 'flutter']):
        return 'Mobile'
    elif any(kw in skill_lower for kw in ['database', 'sql', 'mongodb', 'postgresql']):
        return 'Database'
    else:
        return 'Software Development'


def calculate_confidence(mention_count: int) -> str:
    """Calculate confidence level in forecast.
    
    Args:
        mention_count: Times skill was mentioned
        
    Returns:
        Confidence level
    """
    if mention_count >= 10:
        return 'high'
    elif mention_count >= 5:
        return 'medium'
    else:
        return 'low'


def format_skill_name(skill: str) -> str:
    """Format skill name for display.
    
    Args:
        skill: Raw skill name
        
    Returns:
        Formatted name
    """
    # Already formatted from dictionary
    return skill


def generate_fallback_forecasts() -> List[Dict[str, Any]]:
    """Generate fallback forecasts when Tavily is unavailable.
    
    Returns:
        List of default skill forecasts
    """
    return [
        {
            'skill': 'Artificial Intelligence',
            'current_demand': 85,
            'forecast_demand': 95,
            'growth_rate': '+10%',
            'trend': 'up',
            'category': 'AI/ML',
            'confidence': 'high',
            'source': 'Default Forecast',
            'analyzed_at': datetime.now().isoformat()
        },
        {
            'skill': 'Python',
            'current_demand': 80,
            'forecast_demand': 90,
            'growth_rate': '+10%',
            'trend': 'up',
            'category': 'Programming',
            'confidence': 'high',
            'source': 'Default Forecast',
            'analyzed_at': datetime.now().isoformat()
        },
        {
            'skill': 'Cloud Computing',
            'current_demand': 78,
            'forecast_demand': 88,
            'growth_rate': '+10%',
            'trend': 'up',
            'category': 'Cloud/DevOps',
            'confidence': 'high',
            'source': 'Default Forecast',
            'analyzed_at': datetime.now().isoformat()
        }
    ]


if __name__ == "__main__":
    """Test the skill forecast analyzer."""
    print("=" * 80)
    print("SKILL FORECAST ANALYZER - Testing")
    print("=" * 80)
    
    forecasts = analyze_skill_forecast(max_skills=10)
    
    print(f"\n📊 Generated {len(forecasts)} skill forecasts:\n")
    
    for i, forecast in enumerate(forecasts, 1):
        print(f"{i}. {forecast['skill']}")
        print(f"   Current Demand: {forecast['current_demand']}/100")
        print(f"   Forecast Demand: {forecast['forecast_demand']}/100")
        print(f"   Growth: {forecast['growth_rate']}")
        print(f"   Category: {forecast['category']}")
        print(f"   Confidence: {forecast['confidence'].upper()}")
        print(f"   Source: {forecast['source']}\n")

