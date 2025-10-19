"""
MoneyMentor - LangChain Tool Definitions

Defines lightweight LangChain-compatible tools for GPT-nano orchestration.
Each tool wraps an async function that performs a specific task:
- Finance calculations
- Live web search via Tavily
- RAG-based knowledge retrieval
"""
import os
import sys
import logging
from typing import Optional
from pathlib import Path
from langchain.tools import Tool
from langchain_community.tools.tavily_search import TavilySearchResults

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import existing modules
try:
    # Try relative import (when used as module)
    from .finance_calculator_agent import run_calculation_query
except ImportError:
    # Fall back to absolute import (when run as script)
    from agents.finance_calculator_agent import run_calculation_query

from rag_pipeline import get_finance_answer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable to track tools invoked (for source attribution)
_tools_invoked = []


def get_last_tool_invoked() -> Optional[str]:
    """Get the last tool that was invoked"""
    return _tools_invoked[-1] if _tools_invoked else None


def get_all_tools_invoked() -> list:
    """Get all tools that were invoked"""
    return _tools_invoked.copy()


def reset_last_tool_invoked():
    """Reset the tool tracker"""
    global _tools_invoked
    _tools_invoked = []


# ============================================================================
# Tool Implementation Functions
# ============================================================================

def run_finance_calculator(query: str) -> str:
    """
    Handle financial calculation queries using the finance calculator agent.
    
    Examples:
    - "If I invest $500/month at 7% for 20 years, how much will I have?"
    - "Calculate compound interest on $10,000 at 5% for 10 years"
    
    Args:
        query: Natural language financial calculation query
        
    Returns:
        Concise plain-English result with calculations
    """
    global _tools_invoked
    _tools_invoked.append("finance_calculator_tool")
    print(f"🧰 Tool invoked: finance_calculator_tool for query: {query[:50]}...")
    
    try:
        # Call existing calculator agent
        result = run_calculation_query(query)
        
        if result.get("success"):
            # Format the response in plain English
            explanation = result.get("explanation", "")
            return f"✅ {explanation}"
        else:
            return f"❌ Could not parse calculation from query. Please provide details like amount, rate, and time period."
            
    except Exception as e:
        logger.error(f"Error in finance_calculator: {e}")
        return f"❌ Calculator error: {str(e)}"


def run_tavily_search(query: str) -> str:
    """
    Search live web data using Tavily API.
    
    Use this for:
    - Current financial news
    - Real-time market data
    - Recent policy changes
    - Current interest rates
    
    Args:
        query: Search query
        
    Returns:
        Top 1-2 summaries (< 300 chars total)
    """
    global _tools_invoked
    _tools_invoked.append("tavily_search_tool")
    print(f"🧰 Tool invoked: tavily_search_tool for query: {query[:50]}...")
    
    try:
        # Check for API key
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            logger.warning("⚠️  TAVILY_API_KEY not set")
            return "❌ Tavily search unavailable: API key not configured."
        
        # Initialize Tavily search
        search = TavilySearchResults(
            max_results=2,
            search_depth="basic",
            include_answer=True,
            include_raw_content=False,
            api_key=api_key
        )
        
        # Perform search
        results = search.invoke({"query": query})
        
        if not results:
            return "No results found."
        
        # Format results (keep it concise)
        summaries = []
        for i, result in enumerate(results[:2], 1):
            if isinstance(result, dict):
                content = result.get("content", "")
                url = result.get("url", "")
                # Truncate to ~150 chars per result
                snippet = content[:150] + "..." if len(content) > 150 else content
                summaries.append(f"{i}. {snippet}\n   Source: {url}")
            else:
                summaries.append(f"{i}. {str(result)[:150]}")
        
        return "\n\n".join(summaries)
        
    except Exception as e:
        logger.error(f"Error in tavily_search: {e}")
        return f"❌ Search error: {str(e)}"


def run_rag_answer(query: str) -> str:
    """
    Answer educational finance questions using RAG pipeline.
    
    Use this for:
    - "What is a 401k?"
    - "Explain compound interest"
    - "How do I create a budget?"
    
    Args:
        query: Financial education question
        
    Returns:
        Answer text from knowledge base
    """
    global _tools_invoked
    _tools_invoked.append("rag_tool")
    print(f"🧰 Tool invoked: rag_tool for query: {query[:50]}...")
    
    try:
        # Call RAG pipeline
        result = get_finance_answer(query, k=5)
        
        # Extract just the answer text
        answer = result.get("answer", "No answer found.")
        
        # Optionally include top source
        sources = result.get("sources", [])
        if sources and len(sources) > 0:
            top_source = sources[0].get("source", "")
            answer += f"\n\n📚 Source: {top_source}"
        
        return answer
        
    except Exception as e:
        logger.error(f"Error in rag_answer: {e}")
        return f"❌ RAG error: {str(e)}"


# ============================================================================
# LangChain Tool Definitions
# ============================================================================

finance_calculator_tool = Tool(
    name="finance_calculator_tool",
    description=(
        "Compute investment growth, savings returns, compound interest, and future value calculations. "
        "Use this when the user asks 'how much will I have if I invest...', 'calculate compound interest', "
        "or provides specific numbers for monthly contributions, interest rates, and time periods."
    ),
    func=run_finance_calculator,
)

search_tool = Tool(
    name="tavily_search_tool",
    description=(
        "Search live financial data, current events, recent market news, and real-time information. "
        "Use this when the user asks about 'current interest rates', 'recent financial news', "
        "'latest market trends', or anything requiring up-to-date information from the web."
    ),
    func=run_tavily_search,
)

rag_tool = Tool(
    name="rag_tool",
    description=(
        "Answer educational finance questions from the knowledge base. "
        "Use this for conceptual questions like 'what is a 401k?', 'explain budgeting', "
        "'how does compound interest work?', or any general financial literacy questions."
    ),
    func=run_rag_answer,
)


# ============================================================================
# Export All Tools
# ============================================================================

ALL_TOOLS = [
    finance_calculator_tool,
    search_tool,
    rag_tool,
]


# ============================================================================
# Tool Registry (for debugging/introspection)
# ============================================================================

def list_available_tools() -> None:
    """Print all available tools and their descriptions."""
    print("=" * 70)
    print("Available Tools for MoneyMentor Agent")
    print("=" * 70)
    for tool in ALL_TOOLS:
        print(f"\n🛠️  {tool.name}")
        print(f"   Description: {tool.description}")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    """
    CLI test harness for tools
    """
    print("Testing MoneyMentor Tools\n")
    
    # List available tools
    list_available_tools()
    
    # Test finance calculator
    print("\n" + "=" * 70)
    print("TEST 1: Finance Calculator")
    print("=" * 70)
    calc_result = run_finance_calculator(
        "If I invest $500 a month at 7% for 20 years, how much will I have?"
    )
    print(calc_result)
    
    # Test RAG
    print("\n" + "=" * 70)
    print("TEST 2: RAG Knowledge Base")
    print("=" * 70)
    rag_result = run_rag_answer("What is a budget?")
    print(rag_result[:300] + "..." if len(rag_result) > 300 else rag_result)
    
    # Test Tavily (will fail if no API key, which is expected)
    print("\n" + "=" * 70)
    print("TEST 3: Tavily Search")
    print("=" * 70)
    search_result = run_tavily_search("current fed interest rates 2024")
    print(search_result)
    
    print("\n" + "=" * 70)
    print("✅ Tool testing complete!")
    print("=" * 70)

