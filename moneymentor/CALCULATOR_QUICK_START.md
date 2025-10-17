# Financial Calculator - Quick Start Guide

## 🚀 Test It Now

```bash
cd /Users/amar.kulkarni/code/money-mentor-app/moneymentor

# Run demo
python app/agents/finance_calculator_agent.py

# Run tests
python test_calculator_agent.py
```

---

## 💡 Use in Python

```python
from agents import run_calculation_query

# Ask a question
result = run_calculation_query(
    "If I invest $500 a month at 7% for 20 years, how much?"
)

# Get result
if result['success']:
    print(f"Result: ${result['result']:,.2f}")
    print(result['explanation'])
```

**Output:**
```
Result: $260,463.33
Investing $500.00/month at 7.0% annual return for 20 years:
• Total contributions: $120,000.00
• Interest earned: $140,463.33
• Final value: $260,463.33
Your money will grow 2.17x through compound interest!
```

---

## 📝 Query Formats

**All of these work:**

```python
"If I invest $500 a month at 7% for 20 years, how much?"
"Invest 1000 per month at 8% for 30 years"
"$750/month at 7.5% return for 25 years"
"500 monthly at 5% for 10 years"
"What if I save $200 per month at 6% for 15 years?"
```

---

## 🔧 Direct Calculation

```python
from agents import calculate_future_value

fv, explanation = calculate_future_value(
    monthly_contrib=500,
    annual_rate=7,
    years=20
)

print(f"Future Value: ${fv:,.2f}")
```

---

## 🌐 API Integration

Add to `app/main.py`:

```python
from agents import run_calculation_query

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    # Check if calculation query
    if any(kw in request.question.lower() 
           for kw in ['invest', 'save', 'calculate']):
        
        result = run_calculation_query(request.question)
        if result['success']:
            return ChatResponse(
                answer=result['explanation'],
                sources=[{'source': 'calculator', 
                         'text': str(result['parameters'])}],
                query=request.question
            )
    
    # Fall back to RAG
    return get_finance_answer(request.question)
```

---

## 📊 What You Get

```python
{
    'success': True,
    'result': 260463.33,
    'explanation': "Investing $500.00/month at 7%...",
    'parameters': {
        'monthly_contrib': 500.0,
        'annual_rate': 7.0,
        'years': 20
    }
}
```

---

## 📚 Full Documentation

- **Complete docs:** `app/agents/README.md`
- **Summary:** `CALCULATOR_AGENT_SUMMARY.md`
- **This guide:** `CALCULATOR_QUICK_START.md`

---

## ✅ Ready to Use!

The calculator is fully functional and tested. Integrate it when you're ready!

