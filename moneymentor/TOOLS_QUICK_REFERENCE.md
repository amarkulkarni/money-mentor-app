# MoneyMentor Tools - Quick Reference Card

## 🚀 Quick Start

### Test Individual Tools
```bash
cd moneymentor
source venv/bin/activate
export $(cat .env | grep -v '^#' | xargs)
python demo_agent.py --mode tools
```

### Run Interactive Agent Demo
```bash
python demo_agent.py --mode agent
```

---

## 🛠️ The Three Tools

| Tool | Purpose | Example Query |
|------|---------|--------------|
| 🔢 **Calculator** | Investment calculations | "If I invest $500/mo at 7% for 20y?" |
| 🔍 **Search** | Live web data | "Current fed interest rate?" |
| 📚 **RAG** | Knowledge base | "What is a 401k?" |

---

## 📦 Import Patterns

### Import All Tools
```python
from app.agents import ALL_TOOLS
```

### Import Individual Tools
```python
from app.agents import (
    finance_calculator_tool,
    search_tool,
    rag_tool
)
```

### Import Functions Directly
```python
from app.agents.tools import (
    run_finance_calculator,
    run_tavily_search,
    run_rag_answer
)
```

---

## 💻 Code Examples

### 1. Use with LangChain Agent
```python
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from app.agents import ALL_TOOLS

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
agent = initialize_agent(
    tools=ALL_TOOLS,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

response = agent.run("Calculate $500/mo at 7% for 20 years")
```

### 2. Use Tools Directly (Async)
```python
import asyncio
from app.agents.tools import run_finance_calculator

result = asyncio.run(run_finance_calculator(
    "If I invest $500/month at 7% for 20 years?"
))
print(result)
```

### 3. Multiple Queries
```python
queries = [
    "Calculate $1000/mo at 8% for 15y",
    "What is compound interest?",
    "Current inflation rate"
]

for query in queries:
    response = agent.run(query)
    print(f"Q: {query}\nA: {response}\n")
```

---

## ⚙️ Configuration

### Required Environment Variables
```env
OPENAI_API_KEY=sk-...          # Required
QDRANT_URL=http://localhost:6333  # Required
```

### Optional Environment Variables
```env
TAVILY_API_KEY=tvly-...        # For web search (optional)
```

---

## 📝 Tool Descriptions (for LLM)

These descriptions guide the agent's tool selection:

**finance_calculator_tool**:
> "Compute investment growth, savings returns, compound interest, and future value calculations. Use when user asks 'how much will I have if I invest...'"

**tavily_search_tool**:
> "Search live financial data, current events, recent market news. Use for 'current interest rates', 'recent financial news', etc."

**rag_tool**:
> "Answer educational finance questions from knowledge base. Use for 'what is a 401k?', 'explain budgeting', etc."

---

## 🔍 Testing

### Run Built-in Tests
```bash
cd moneymentor/app
python -m agents.tools
```

### Expected Output
```
✅ finance_calculator_tool - Working
✅ rag_tool - Working
⚠️  tavily_search_tool - No API key (expected)
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Import error | `cd moneymentor/app && python -m agents.tools` |
| Calculator fails | Check query format: "$500/month at 7% for 20 years" |
| RAG returns nothing | Ensure Qdrant is running and indexed |
| Search fails | Set `TAVILY_API_KEY` in `.env` |

---

## 📚 Documentation

- **Full Guide**: `TOOLS_USAGE.md`
- **Implementation**: `TOOLS_IMPLEMENTATION_SUMMARY.md`
- **Code**: `app/agents/tools.py`
- **Demo**: `demo_agent.py`

---

## ✅ Checklist

Before using in production:

- [ ] `OPENAI_API_KEY` set in `.env`
- [ ] Qdrant running (`./qdrant` or Docker)
- [ ] Knowledge base loaded (`curl -X POST localhost:8000/api/reload_knowledge`)
- [ ] Test tools: `python -m agents.tools`
- [ ] (Optional) `TAVILY_API_KEY` for search

---

## 🎯 When to Use Each Tool

**Use Calculator** when query has:
- Numbers (amount, rate, time)
- Keywords: "invest", "calculate", "how much", "grow"
- Mathematical operations

**Use Search** when query asks about:
- "Current", "latest", "recent", "today"
- Real-time data
- News or events

**Use RAG** when query asks:
- "What is...", "Explain...", "How does..."
- Concepts, definitions, education
- General financial knowledge

---

**Last Updated**: October 19, 2025  
**Version**: 1.0  
**Status**: Production Ready ✅

