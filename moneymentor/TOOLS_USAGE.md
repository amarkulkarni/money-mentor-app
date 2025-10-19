# MoneyMentor Tools - Usage Guide

## Overview

MoneyMentor provides **3 LangChain-compatible tools** for orchestrating GPT-based financial agents:

1. **Finance Calculator Tool** - Compute investment growth and returns
2. **Tavily Search Tool** - Search live web data for current information
3. **RAG Tool** - Answer questions from the knowledge base

---

## Installation

Ensure you have the required dependencies:

```bash
pip install -r requirements.txt
```

Set up your environment variables in `.env`:

```env
OPENAI_API_KEY=sk-...
QDRANT_URL=http://localhost:6333
TAVILY_API_KEY=tvly-...  # Optional, for web search
```

---

## Quick Start

### Using Individual Tools

```python
import asyncio
from app.agents.tools import (
    run_finance_calculator,
    run_tavily_search,
    run_rag_answer
)

# Test calculator
result = asyncio.run(run_finance_calculator(
    "If I invest $500/month at 7% for 20 years, how much?"
))
print(result)

# Test RAG
result = asyncio.run(run_rag_answer("What is a budget?"))
print(result)

# Test search (requires TAVILY_API_KEY)
result = asyncio.run(run_tavily_search("current fed interest rates"))
print(result)
```

### Using LangChain Agent

```python
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from app.agents import ALL_TOOLS

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Create agent with all tools
agent = initialize_agent(
    tools=ALL_TOOLS,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Run query
response = agent.run(
    "If I invest $1000/month at 8% for 15 years, "
    "what will I have? Also, what's a good budgeting strategy?"
)
print(response)
```

---

## Tool Descriptions

### 1. Finance Calculator Tool

**Name**: `finance_calculator_tool`

**Description**: Compute investment growth, savings returns, compound interest, and future value calculations.

**Best For**:
- "If I invest $X per month at Y% for Z years, how much will I have?"
- "Calculate compound interest on $10,000 at 5% for 10 years"
- Investment projections
- Retirement savings calculations

**Example**:
```python
await run_finance_calculator(
    "Calculate how much I'll have if I invest $500/month at 7% for 20 years"
)
```

**Output**:
```
✅ Investing $500.00/month at 7.0% annual return for 20 years:
• Total contributions: $120,000.00
• Interest earned: $140,463.33
• Final value: $260,463.33
Your money will grow 2.17x through compound interest!
```

---

### 2. Tavily Search Tool

**Name**: `tavily_search_tool`

**Description**: Search live financial data, current events, recent market news, and real-time information.

**Best For**:
- Current interest rates
- Recent financial news
- Market trends
- Policy changes
- Stock prices

**Requires**: `TAVILY_API_KEY` environment variable

**Example**:
```python
await run_tavily_search("current federal reserve interest rate 2024")
```

**Output**:
```
1. The Federal Reserve held interest rates steady at 5.25%-5.50% in October 2024...
   Source: https://www.federalreserve.gov/...

2. Fed officials signal cautious approach to rate cuts amid inflation concerns...
   Source: https://www.reuters.com/...
```

---

### 3. RAG Tool

**Name**: `rag_tool`

**Description**: Answer educational finance questions from the MoneyMentor knowledge base.

**Best For**:
- "What is a 401k?"
- "Explain compound interest"
- "How do I create a budget?"
- "What are mutual funds?"
- General financial literacy questions

**Example**:
```python
await run_rag_answer("What is compound interest and how does it work?")
```

**Output**:
```
Compound interest is the interest calculated on both the initial principal 
and the accumulated interest from previous periods. This means your money 
grows faster over time because you earn interest on your interest...

📚 Source: financialliteracy101.txt
```

---

## Advanced Usage

### Custom Agent with Selected Tools

```python
from app.agents import finance_calculator_tool, rag_tool

# Use only specific tools
custom_tools = [finance_calculator_tool, rag_tool]

agent = initialize_agent(
    tools=custom_tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)
```

### Programmatic Tool Access

```python
from app.agents import list_available_tools

# List all available tools
list_available_tools()

# Access tools programmatically
from app.agents import ALL_TOOLS

for tool in ALL_TOOLS:
    print(f"Tool: {tool.name}")
    print(f"Description: {tool.description}")
```

---

## Testing

Run the built-in test suite:

```bash
cd moneymentor/app
python -m agents.tools
```

Expected output:
```
Testing MoneyMentor Tools

======================================================================
Available Tools for MoneyMentor Agent
======================================================================

🛠️  finance_calculator_tool
   Description: Compute investment growth...

[Test results for all three tools]

✅ Tool testing complete!
```

---

## Tool Selection Logic

When building an agent, the LLM will automatically select the appropriate tool based on the query:

| Query Type | Selected Tool | Example |
|-----------|--------------|---------|
| **Calculation** | `finance_calculator_tool` | "How much will I have if I invest..." |
| **Current Info** | `tavily_search_tool` | "What's the current inflation rate?" |
| **Education** | `rag_tool` | "What is a Roth IRA?" |

---

## Environment Variables

| Variable | Required | Purpose | Default |
|----------|----------|---------|---------|
| `OPENAI_API_KEY` | Yes | GPT API access | - |
| `QDRANT_URL` | Yes | Vector DB connection | `http://localhost:6333` |
| `TAVILY_API_KEY` | No | Web search functionality | - |

**Note**: If `TAVILY_API_KEY` is not set, the search tool will return an error message but won't crash.

---

## Error Handling

All tools include graceful error handling:

```python
# Calculator with invalid query
result = await run_finance_calculator("hello world")
# Returns: "❌ Could not parse calculation from query..."

# Search without API key
result = await run_tavily_search("anything")
# Returns: "❌ Tavily search unavailable: API key not configured."

# RAG with no results
result = await run_rag_answer("asdfghjkl")
# Returns a response indicating no relevant information found
```

---

## Performance Notes

- **Calculator**: Instant (<10ms)
- **RAG**: ~500-1000ms (embedding + search + LLM)
- **Search**: ~1-2 seconds (API call to Tavily)

---

## Next Steps

1. **Add More Tools**: Create custom tools for specific financial needs
2. **Fine-tune Descriptions**: Improve tool selection accuracy
3. **Add Caching**: Cache frequent queries for faster responses
4. **Multi-step Reasoning**: Implement sequential tool use with LangChain agents

---

## Troubleshooting

### Import Errors
```bash
# If you get import errors, ensure you're in the correct directory
cd moneymentor/app
python -m agents.tools
```

### Tool Not Being Selected
- Check tool descriptions - they guide the LLM's decision
- Use more explicit queries
- Increase LLM temperature for more creative tool selection

### Tavily Search Not Working
- Verify `TAVILY_API_KEY` is set in `.env`
- Check API key is valid at https://tavily.com
- Free tier has rate limits (50 requests/month)

---

## API Reference

See individual tool implementations in `app/agents/tools.py` for detailed documentation.

For calculator formulas, see `app/agents/finance_calculator_agent.py`.

For RAG pipeline details, see `app/rag_pipeline.py`.

