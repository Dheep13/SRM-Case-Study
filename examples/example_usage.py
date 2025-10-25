"""Example usage of GenAI Learning and Trend Analysis Agents."""

from agents.orchestrator import GenAIAgentOrchestrator
from agents.content_scraper_agent import ContentScraperAgent
from agents.trend_analysis_agent import TrendAnalysisAgent
import json


def example_1_full_orchestration():
    """Example 1: Run both agents through the orchestrator."""
    print("\n" + "="*80)
    print("Example 1: Full Orchestration - Learning Resources + Trends")
    print("="*80)
    
    orchestrator = GenAIAgentOrchestrator()
    
    query = "LangChain and LangGraph tutorials"
    
    # Get JSON report
    report = orchestrator.run(query, output_format="json")
    
    # Display summary
    print(f"\nQuery: {report['query']}")
    print(f"Learning Resources: {report['summary']['total_learning_resources']}")
    print(f"Trending Topics: {report['summary']['total_trending_topics']}")
    
    print("\nTop 3 Learning Resources:")
    for i, resource in enumerate(report['learning_resources'][:3], 1):
        print(f"{i}. {resource['title']}")
        print(f"   Category: {resource['category']}")
        print(f"   URL: {resource['url']}\n")
    
    print("\nTop 3 Trending Topics:")
    for i, trend in enumerate(report['trending_topics'][:3], 1):
        print(f"{i}. {trend['title']}")
        print(f"   Source: {trend['source']}")
        print(f"   Score: {trend['overall_score']:.2f}\n")
    
    print("\nInsights:")
    print(report['insights'])
    
    # Save report
    orchestrator.save_report(report, "example_full_report.json")


def example_2_content_only():
    """Example 2: Run only the Content Scraper Agent."""
    print("\n" + "="*80)
    print("Example 2: Content Scraper Agent Only")
    print("="*80)
    
    agent = ContentScraperAgent()
    
    query = "RAG retrieval augmented generation"
    resources = agent.run(query)
    
    print(f"\nFound {len(resources)} learning resources for: {query}\n")
    
    for i, resource in enumerate(resources[:5], 1):
        print(f"{i}. {resource['title']}")
        print(f"   Category: {resource['category']}")
        print(f"   Relevance: {resource['relevance_score']:.2f}")
        print(f"   Source: {resource['source']}")
        print(f"   URL: {resource['url']}\n")


def example_3_trends_only():
    """Example 3: Run only the Trend Analysis Agent."""
    print("\n" + "="*80)
    print("Example 3: Trend Analysis Agent Only")
    print("="*80)
    
    agent = TrendAnalysisAgent()
    
    topic = "GenAI"
    trends = agent.run(topic)
    
    print(f"\nFound {len(trends)} trending topics for: {topic}\n")
    
    # Group by source
    github_trends = [t for t in trends if t['source'] == 'GitHub']
    linkedin_trends = [t for t in trends if t['source'] == 'LinkedIn']
    
    print(f"GitHub Trends ({len(github_trends)}):")
    for i, trend in enumerate(github_trends[:3], 1):
        print(f"{i}. {trend['title']}")
        print(f"   Stars: {trend['metrics'].get('stars', 'N/A')}")
        print(f"   Language: {trend['metrics'].get('language', 'N/A')}")
        print(f"   Score: {trend['overall_score']:.2f}\n")
    
    print(f"LinkedIn Trends ({len(linkedin_trends)}):")
    for i, trend in enumerate(linkedin_trends[:3], 1):
        print(f"{i}. {trend['title']}")
        print(f"   Estimated Posts: {trend['metrics'].get('estimated_posts', 'N/A')}")
        print(f"   Score: {trend['overall_score']:.2f}\n")


def example_4_multiple_queries():
    """Example 4: Process multiple queries."""
    print("\n" + "="*80)
    print("Example 4: Multiple Query Analysis")
    print("="*80)
    
    orchestrator = GenAIAgentOrchestrator()
    
    queries = [
        "prompt engineering",
        "vector databases",
        "AI agents"
    ]
    
    results = []
    
    for query in queries:
        print(f"\nProcessing: {query}")
        report = orchestrator.run(query, output_format="json")
        
        results.append({
            'query': query,
            'resources_count': len(report['learning_resources']),
            'trends_count': len(report['trending_topics']),
            'top_resource': report['learning_resources'][0] if report['learning_resources'] else None,
            'top_trend': report['trending_topics'][0] if report['trending_topics'] else None
        })
    
    print("\n" + "="*80)
    print("Summary of All Queries:")
    print("="*80)
    
    for result in results:
        print(f"\nQuery: {result['query']}")
        print(f"  Resources: {result['resources_count']}")
        print(f"  Trends: {result['trends_count']}")
        if result['top_resource']:
            print(f"  Top Resource: {result['top_resource']['title']}")
        if result['top_trend']:
            print(f"  Top Trend: {result['top_trend']['title']}")


def example_5_text_report():
    """Example 5: Generate text format report."""
    print("\n" + "="*80)
    print("Example 5: Text Format Report")
    print("="*80)
    
    orchestrator = GenAIAgentOrchestrator()
    
    query = "GenAI best practices"
    text_report = orchestrator.run(query, output_format="text")
    
    print(text_report)
    
    # Save text report
    with open("example_text_report.txt", "w", encoding="utf-8") as f:
        f.write(text_report)
    print("\nText report saved to: example_text_report.txt")


def run_all_examples():
    """Run all examples sequentially."""
    print("\n" + "#"*80)
    print("# GenAI Learning & Trend Analysis Agents - Examples")
    print("#"*80)
    
    examples = [
        ("Full Orchestration", example_1_full_orchestration),
        ("Content Scraper Only", example_2_content_only),
        ("Trend Analysis Only", example_3_trends_only),
        ("Multiple Queries", example_4_multiple_queries),
        ("Text Report", example_5_text_report)
    ]
    
    print("\nAvailable Examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")
    
    print("\nRunning Example 1 (Full Orchestration)...")
    example_1_full_orchestration()
    
    print("\n\nTo run other examples, modify the script or call them individually:")
    print("  python example_usage.py")


if __name__ == "__main__":
    try:
        # Run the main orchestration example
        run_all_examples()
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nPlease ensure:")
        print("1. Create a .env file with your OPENAI_API_KEY")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Copy .env.example to .env and fill in your API keys")

