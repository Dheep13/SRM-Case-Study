"""Main Orchestrator for coordinating GenAI Learning and Trend Analysis agents."""

from typing import Dict, Any, TypedDict
from datetime import datetime
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from agents.content_scraper_agent import ContentScraperAgent
from agents.trend_analysis_agent import TrendAnalysisAgent
import config


class OrchestratorState(TypedDict):
    """State for the main orchestrator."""
    query: str
    learning_resources: list
    trending_topics: list
    final_report: Dict[str, Any]
    error: str


class GenAIAgentOrchestrator:
    """Orchestrator for coordinating multiple GenAI agents."""
    
    def __init__(self):
        """Initialize the orchestrator with both agents."""
        config.validate_config()
        
        self.content_agent = ContentScraperAgent()
        self.trend_agent = TrendAnalysisAgent()
        self.llm = None  # Lazy init
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the orchestrator workflow graph."""
        workflow = StateGraph(OrchestratorState)
        
        # Define nodes
        workflow.add_node("content_search", self._content_search_node)
        workflow.add_node("trend_analysis", self._trend_analysis_node)
        workflow.add_node("generate_report", self._generate_report_node)
        
        # Define edges - run agents in parallel conceptually, but sequentially here
        workflow.set_entry_point("content_search")
        workflow.add_edge("content_search", "trend_analysis")
        workflow.add_edge("trend_analysis", "generate_report")
        workflow.add_edge("generate_report", END)
        
        return workflow.compile()
    
    def _content_search_node(self, state: OrchestratorState) -> OrchestratorState:
        """Execute content scraper agent."""
        print(f"\n[Orchestrator] Running Content Scraper Agent for: {state['query']}")
        
        try:
            resources = self.content_agent.run(state['query'])
            state['learning_resources'] = resources
            print(f"[Orchestrator] Found {len(resources)} learning resources")
        except Exception as e:
            state['error'] = f"Content search failed: {str(e)}"
            state['learning_resources'] = []
            print(f"[Orchestrator] Error: {state['error']}")
        
        return state
    
    def _trend_analysis_node(self, state: OrchestratorState) -> OrchestratorState:
        """Execute trend analysis agent."""
        print(f"\n[Orchestrator] Running Trend Analysis Agent for: {state['query']}")
        
        try:
            trends = self.trend_agent.run(state['query'])
            state['trending_topics'] = trends
            print(f"[Orchestrator] Found {len(trends)} trending topics")
        except Exception as e:
            state['error'] = f"Trend analysis failed: {str(e)}"
            state['trending_topics'] = []
            print(f"[Orchestrator] Error: {state['error']}")
        
        return state
    
    def _generate_report_node(self, state: OrchestratorState) -> OrchestratorState:
        """Generate final report combining both agents' results."""
        print("\n[Orchestrator] Generating final report...")
        
        resources = state.get('learning_resources', [])
        trends = state.get('trending_topics', [])
        
        # Use LLM to generate insights
        try:
            insights = self._generate_insights(resources, trends, state['query'])
        except Exception as e:
            insights = f"Failed to generate insights: {str(e)}"
        
        report = {
            'query': state['query'],
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_learning_resources': len(resources),
                'total_trending_topics': len(trends),
                'top_categories': self._get_top_categories(resources),
                'top_platforms': self._get_top_platforms(trends)
            },
            'learning_resources': resources[:10],  # Top 10 resources
            'trending_topics': trends[:15],  # Top 15 trends
            'insights': insights,
            'errors': state.get('error', '')
        }
        
        state['final_report'] = report
        print("[Orchestrator] Report generation complete")
        
        return state
    
    def _generate_insights(self, resources: list, trends: list, query: str) -> str:
        """Generate insights using LLM based on collected data - OPTIMIZED."""
        if not self.llm:
            try:
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    model="gpt-4o-mini",
                    temperature=0.7,
                    max_tokens=300,
                    api_key=config.OPENAI_API_KEY
                )
            except ImportError:
                return f"Found {len(resources)} resources and {len(trends)} trends for '{query}'."

        prompt = ChatPromptTemplate.from_messages([
            ("system", """Expert GenAI analyst. Give 3-4 bullet points on: learning paths, trending topics, recommended resources, industry focus."""),
            ("user", """Query: {query}
Resources ({resource_count}): {top_resources}
Trends ({trend_count}): {top_trends}

Brief analysis:""")
        ])

        top_resources = [r.get('title', '') for r in resources[:3]]
        top_trends = [t.get('title', '') for t in trends[:3]]

        try:
            response = self.llm.invoke(
                prompt.format_messages(
                    query=query,
                    resource_count=len(resources),
                    top_resources=", ".join(top_resources) if top_resources else "None found",
                    trend_count=len(trends),
                    top_trends=", ".join(top_trends) if top_trends else "None found"
                )
            )
            return response.content
        except Exception as e:
            return f"Insights generation failed: {str(e)}"
    
    def _get_top_categories(self, resources: list) -> Dict[str, int]:
        """Get distribution of content categories."""
        categories = {}
        for resource in resources:
            category = resource.get('category', 'unknown')
            categories[category] = categories.get(category, 0) + 1
        
        return dict(sorted(categories.items(), key=lambda x: x[1], reverse=True))
    
    def _get_top_platforms(self, trends: list) -> Dict[str, int]:
        """Get distribution of trend sources."""
        platforms = {}
        for trend in trends:
            source = trend.get('source', 'unknown')
            platforms[source] = platforms.get(source, 0) + 1
        
        return dict(sorted(platforms.items(), key=lambda x: x[1], reverse=True))
    
    def run(self, query: str, output_format: str = "json") -> Dict[str, Any]:
        """Run the orchestrator with both agents.
        
        Args:
            query: Search query for GenAI content and trends
            output_format: Output format - 'json' or 'text'
            
        Returns:
            Final report with all findings
        """
        print(f"\n{'='*80}")
        print(f"GenAI Agent Orchestrator - Starting Analysis")
        print(f"Query: {query}")
        print(f"{'='*80}")
        
        initial_state = OrchestratorState(
            query=query,
            learning_resources=[],
            trending_topics=[],
            final_report={},
            error=""
        )
        
        result = self.graph.invoke(initial_state)
        report = result.get('final_report', {})
        
        if output_format == "text":
            return self._format_text_report(report)
        
        return report
    
    def _format_text_report(self, report: Dict[str, Any]) -> str:
        """Format report as human-readable text."""
        text = f"\n{'='*80}\n"
        text += f"GenAI Learning & Trend Analysis Report\n"
        text += f"{'='*80}\n\n"
        
        text += f"Query: {report.get('query', 'N/A')}\n"
        text += f"Generated: {report.get('generated_at', 'N/A')}\n\n"
        
        summary = report.get('summary', {})
        text += f"Summary:\n"
        text += f"  - Learning Resources Found: {summary.get('total_learning_resources', 0)}\n"
        text += f"  - Trending Topics Found: {summary.get('total_trending_topics', 0)}\n"
        text += f"  - Top Categories: {', '.join(summary.get('top_categories', {}).keys())}\n"
        text += f"  - Top Platforms: {', '.join(summary.get('top_platforms', {}).keys())}\n\n"
        
        text += f"Insights:\n{report.get('insights', 'No insights available')}\n\n"
        
        text += f"\nTop Learning Resources:\n"
        text += f"{'-'*80}\n"
        for i, resource in enumerate(report.get('learning_resources', [])[:5], 1):
            text += f"{i}. {resource.get('title', 'N/A')}\n"
            text += f"   URL: {resource.get('url', 'N/A')}\n"
            text += f"   Category: {resource.get('category', 'N/A')}\n"
            text += f"   Description: {resource.get('description', 'N/A')[:100]}...\n\n"
        
        text += f"\nTop Trending Topics:\n"
        text += f"{'-'*80}\n"
        for i, trend in enumerate(report.get('trending_topics', [])[:5], 1):
            text += f"{i}. {trend.get('title', 'N/A')}\n"
            text += f"   Source: {trend.get('source', 'N/A')}\n"
            text += f"   Description: {trend.get('description', 'N/A')[:100]}...\n"
            text += f"   Score: {trend.get('overall_score', 0):.2f}\n\n"
        
        text += f"{'='*80}\n"
        
        return text
    
    def save_report(self, report: Dict[str, Any], filename: str = None):
        """Save report to file.
        
        Args:
            report: Report data to save
            filename: Output filename (auto-generated if not provided)
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"genai_report_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n[Orchestrator] Report saved to: {filename}")


def main():
    """Main entry point for running the orchestrator."""
    try:
        # Initialize orchestrator
        orchestrator = GenAIAgentOrchestrator()
        
        # Example queries
        queries = [
            "LangChain tutorials",
            "RAG implementation",
            "GenAI agent frameworks"
        ]
        
        # Run for first query
        query = queries[0]
        report = orchestrator.run(query, output_format="text")
        
        print(report)
        
        # Save JSON report
        json_report = orchestrator.run(query, output_format="json")
        orchestrator.save_report(json_report)
        
    except Exception as e:
        print(f"\nError running orchestrator: {str(e)}")
        print("\nPlease ensure:")
        print("1. .env file is configured with OPENAI_API_KEY")
        print("2. All dependencies are installed: pip install -r requirements.txt")


if __name__ == "__main__":
    main()