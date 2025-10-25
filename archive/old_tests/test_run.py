"""Simple test script for GenAI agents - outputs JSON to avoid encoding issues."""

import json
from agents.orchestrator import GenAIAgentOrchestrator

def main():
    print("\n" + "="*80)
    print("Testing GenAI Learning & Trend Analysis Agents")
    print("="*80 + "\n")
    
    # Test query
    query = "LangChain tutorials"
    print(f"Query: {query}\n")
    
    try:
        # Initialize orchestrator
        orchestrator = GenAIAgentOrchestrator()
        
        # Run with JSON output to avoid encoding issues
        report = orchestrator.run(query, output_format="json")
        
        # Display summary
        print("="*80)
        print("RESULTS SUMMARY")
        print("="*80)
        print(f"\nQuery: {report['query']}")
        print(f"Generated: {report['generated_at']}")
        print(f"\nLearning Resources Found: {report['summary']['total_learning_resources']}")
        print(f"Trending Topics Found: {report['summary']['total_trending_topics']}")
        
        # Top categories
        print(f"\nTop Categories:")
        for category, count in list(report['summary']['top_categories'].items())[:5]:
            print(f"  - {category}: {count}")
        
        # Top 5 learning resources
        print(f"\n{'='*80}")
        print("TOP 5 LEARNING RESOURCES")
        print("="*80)
        for i, resource in enumerate(report['learning_resources'][:5], 1):
            print(f"\n{i}. {resource['title']}")
            print(f"   Category: {resource['category']}")
            print(f"   Source: {resource['source']}")
            print(f"   Relevance Score: {resource['relevance_score']:.2f}")
            print(f"   URL: {resource['url']}")
            desc = resource.get('description', '')[:100]
            print(f"   Description: {desc}...")
        
        # Top 5 trending topics
        if report['trending_topics']:
            print(f"\n{'='*80}")
            print("TOP 5 TRENDING TOPICS")
            print("="*80)
            for i, trend in enumerate(report['trending_topics'][:5], 1):
                print(f"\n{i}. {trend['title']}")
                print(f"   Source: {trend['source']}")
                print(f"   Type: {trend['type']}")
                print(f"   Overall Score: {trend['overall_score']:.2f}")
                if trend['source'] == 'GitHub':
                    print(f"   Stars: {trend['metrics'].get('stars', 'N/A')}")
                    print(f"   Language: {trend['metrics'].get('language', 'N/A')}")
                desc = trend.get('description', '')[:100]
                print(f"   Description: {desc}...")
        
        # Save the full report
        filename = "test_report.json"
        orchestrator.save_report(report, filename)
        print(f"\n{'='*80}")
        print(f"Full report saved to: {filename}")
        print("="*80)
        
        print("\n[SUCCESS] Test completed successfully!")
        print("\nNext steps:")
        print("1. View the full report in test_report.json")
        print("2. Run 'python -m examples.example_usage' for more examples")
        print("3. Run 'python main.py \"your query\"' for custom queries")
        
    except Exception as e:
        print(f"\n[ERROR] Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

