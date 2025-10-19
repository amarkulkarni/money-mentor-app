"""
MoneyMentor - Agent Orchestrator

Lightweight orchestration layer using LangChain agents for intelligent tool selection.
Uses GPT-4o-mini for reasoning and automatic tool routing.
"""
import os
import logging
from typing import Dict, Any, List, Optional
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.schema import AgentAction, AgentFinish, SystemMessage

from .tools import ALL_TOOLS, get_last_tool_invoked, get_all_tools_invoked, reset_last_tool_invoked

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_agent_query(query: str, verbose: bool = False) -> Dict[str, Any]:
    """
    Run a query through the LangChain agent orchestrator.
    
    The agent will automatically select the appropriate tool(s) based on the query:
    - finance_calculator_tool: For investment calculations
    - tavily_search_tool: For current/live information
    - rag_tool: For educational financial questions
    
    Args:
        query: User's question or request
        verbose: If True, print detailed agent reasoning steps
        
    Returns:
        Dictionary containing:
        - answer: The final response text
        - tool_used: Name of the tool(s) used (or "none" if no tool used)
        - intermediate_steps: List of reasoning steps taken by the agent
        
    Example:
        >>> result = run_agent_query("If I invest $500/mo at 7% for 20y?")
        >>> print(result["answer"])
        >>> print(f"Tool used: {result['tool_used']}")
    """
    try:
        # Reset tool tracker before running
        reset_last_tool_invoked()
        
        # Check for OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("❌ OPENAI_API_KEY not found in environment")
            return {
                "answer": "Sorry, I couldn't complete that. OpenAI API key is not configured.",
                "tool_used": "none",
                "intermediate_steps": None
            }
        
        # Initialize LLM (GPT-4o-mini for fast, cost-effective reasoning)
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,  # Deterministic for consistent tool selection
            openai_api_key=api_key
        )
        
        # Define system message to guide tool usage
        agent_kwargs = {
            "system_message": SystemMessage(content="""
You are a financial advisory assistant with access to specialized tools.

When answering questions, follow these rules:
1. Use rag_tool for definitions, concepts, explanations, and educational content
   - Examples: "What is X?", "Explain Y", "How does Z work?"
2. Use tavily_search_tool for current data, rates, trends, and recent information
   - Examples: "Current rate", "Today's market", "Recent trends"
3. Use finance_calculator_tool for investment calculations and projections
   - Examples: "How much will I have?", "Calculate returns"

IMPORTANT:
- When a question has BOTH educational and current components, use BOTH tools
- Always prefer using tools over your general knowledge
- Cite sources from the tools in your answer
- If unsure which tool to use, use multiple tools

Example:
Question: "What is inflation and what is the current rate?"
→ Use rag_tool first to explain inflation
→ Use tavily_search_tool to get current rate
→ Combine both answers
""")
        }
        
        # Initialize agent with tools and system message
        agent = initialize_agent(
            tools=ALL_TOOLS,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=verbose,
            handle_parsing_errors=True,
            max_iterations=5,  # Limit iterations to prevent runaway loops
            max_execution_time=30,  # 30 second timeout
            early_stopping_method="generate",
            agent_kwargs=agent_kwargs
        )
        
        # Run the agent
        logger.info(f"🤖 Agent processing query: '{query[:60]}...'")
        
        # Use the agent's internal method to get intermediate steps
        result = agent({"input": query})
        
        # Extract answer
        answer = result.get("output", "No response generated.")
        
        # Extract tool usage from intermediate steps
        intermediate_steps = result.get("intermediate_steps", [])
        tools_used = []
        
        if intermediate_steps:
            for step in intermediate_steps:
                if isinstance(step, tuple) and len(step) >= 1:
                    action = step[0]
                    if isinstance(action, AgentAction):
                        tool_name = action.tool
                        tools_used.append(tool_name)
                        print(f"🔍 Agent selected: {tool_name}")
        
        # Determine primary tool used
        if tools_used:
            tool_used = tools_used[0] if len(tools_used) == 1 else ", ".join(tools_used)
        else:
            # Fallback: check global tracker
            tracked_tools = get_all_tools_invoked()
            if tracked_tools:
                tool_used = tracked_tools[0] if len(tracked_tools) == 1 else ", ".join(tracked_tools)
                print(f"🔍 Agent selected: {tool_used} (via tracker)")
            else:
                tool_used = "none"
                print("🔍 Agent selected: none (direct response)")
        
        logger.info(f"✅ Agent completed successfully")
        
        return {
            "answer": answer,
            "tool_used": tool_used,
            "intermediate_steps": [
                {
                    "tool": step[0].tool if isinstance(step[0], AgentAction) else "unknown",
                    "input": step[0].tool_input if isinstance(step[0], AgentAction) else "",
                    "output": str(step[1])[:200] + "..." if len(str(step[1])) > 200 else str(step[1])
                }
                for step in intermediate_steps
                if isinstance(step, tuple) and len(step) >= 2
            ] if intermediate_steps else None
        }
        
    except KeyboardInterrupt:
        logger.warning("⚠️  Agent execution interrupted by user")
        return {
            "answer": "Sorry, I couldn't complete that. Execution was interrupted.",
            "tool_used": "none",
            "intermediate_steps": None
        }
        
    except Exception as e:
        logger.error(f"❌ Error in agent execution: {e}")
        logger.exception("Full traceback:")
        
        return {
            "answer": "Sorry, I couldn't complete that. An error occurred while processing your request.",
            "tool_used": "none",
            "intermediate_steps": None,
            "error": str(e)
        }


def run_agent_batch(queries: List[str], verbose: bool = False) -> List[Dict[str, Any]]:
    """
    Run multiple queries through the agent in sequence.
    
    Args:
        queries: List of user questions
        verbose: If True, print detailed reasoning for each query
        
    Returns:
        List of result dictionaries
        
    Example:
        >>> queries = [
        ...     "Calculate $500/mo at 7% for 20y",
        ...     "What is a 401k?"
        ... ]
        >>> results = run_agent_batch(queries)
    """
    results = []
    
    for i, query in enumerate(queries, 1):
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing query {i}/{len(queries)}")
        logger.info(f"{'='*60}")
        
        result = run_agent_query(query, verbose=verbose)
        results.append(result)
    
    return results


def get_agent_info() -> Dict[str, Any]:
    """
    Get information about the agent configuration.
    
    Returns:
        Dictionary with agent metadata
    """
    return {
        "model": "gpt-4o-mini",
        "agent_type": "ZERO_SHOT_REACT_DESCRIPTION",
        "available_tools": [tool.name for tool in ALL_TOOLS],
        "max_iterations": 5,
        "timeout": 30
    }


if __name__ == "__main__":
    """
    CLI test harness for the agent orchestrator
    """
    print("=" * 70)
    print("MoneyMentor - Agent Orchestrator Test")
    print("=" * 70)
    print()
    
    # Display agent info
    info = get_agent_info()
    print("Agent Configuration:")
    print(f"  Model: {info['model']}")
    print(f"  Type: {info['agent_type']}")
    print(f"  Available tools: {', '.join(info['available_tools'])}")
    print(f"  Max iterations: {info['max_iterations']}")
    print(f"  Timeout: {info['timeout']}s")
    print()
    
    # Test queries
    test_queries = [
        {
            "query": "If I invest $500 per month at 7% for 20 years, how much will I have?",
            "expected_tool": "finance_calculator_tool"
        },
        {
            "query": "What is a budget and why is it important?",
            "expected_tool": "rag_tool"
        },
        {
            "query": "Calculate the future value of $1000/month at 8% for 15 years",
            "expected_tool": "finance_calculator_tool"
        }
    ]
    
    for i, test in enumerate(test_queries, 1):
        print("=" * 70)
        print(f"TEST {i}: {test['query'][:60]}...")
        print(f"Expected tool: {test['expected_tool']}")
        print("=" * 70)
        
        result = run_agent_query(test["query"], verbose=False)
        
        print(f"\n✅ Tool used: {result['tool_used']}")
        print(f"\n📝 Answer:\n{result['answer'][:300]}...")
        
        if result["intermediate_steps"]:
            print(f"\n🔍 Intermediate steps:")
            for step in result["intermediate_steps"]:
                print(f"  • {step['tool']}: {step['input'][:50]}...")
        
        print("\n")
        
    print("=" * 70)
    print("✅ All tests complete!")
    print("=" * 70)

