# LangSmith Setup Guide for MoneyMentor

This guide walks you through setting up LangSmith to track and evaluate MoneyMentor's RAG pipeline.

## What is LangSmith?

LangSmith is LangChain's platform for:
- 🔍 **Tracing**: See every step of your LLM application
- 📊 **Evaluation**: Track metrics over time
- 🐛 **Debugging**: Identify issues in production
- 📈 **Monitoring**: View usage and performance

## Step 1: Create LangSmith Account

1. Go to [smith.langchain.com](https://smith.langchain.com)
2. Sign up with your email or GitHub
3. Create a new project (e.g., "MoneyMentor")

## Step 2: Get Your API Key

1. Click your profile → **Settings**
2. Go to **API Keys**
3. Click **Create API Key**
4. Copy the key (starts with `ls__...`)

## Step 3: Configure Environment Variables

Add these to your `.env` file:

```bash
# LangSmith Configuration
LANGCHAIN_API_KEY=ls__your_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=MoneyMentor
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

### Update your .env file:

```bash
cd /Users/amar.kulkarni/code/money-mentor-app/moneymentor

# Add to .env
cat >> .env << 'EOF'

# LangSmith tracking (optional)
LANGCHAIN_API_KEY=your_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=MoneyMentor
EOF
```

## Step 4: Verify Configuration

Test that LangSmith is configured:

```bash
cd /Users/amar.kulkarni/code/money-mentor-app/moneymentor

python3 << 'EOF'
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("LANGCHAIN_API_KEY")
tracing = os.getenv("LANGCHAIN_TRACING_V2")
project = os.getenv("LANGCHAIN_PROJECT")

print("LangSmith Configuration:")
print(f"  API Key: {'✅ Set' if api_key else '❌ Not set'}")
print(f"  Tracing: {'✅ Enabled' if tracing == 'true' else '❌ Disabled'}")
print(f"  Project: {project or '❌ Not set'}")

if api_key and tracing and project:
    print("\n✅ LangSmith is ready!")
else:
    print("\n❌ Please configure all LangSmith variables")
EOF
```

## Step 5: Run Evaluation with LangSmith

Once configured, your evaluations will automatically log to LangSmith:

```bash
# Make sure backend is running
cd app && python -m uvicorn main:app --reload --port 8000 &

# Run evaluation
cd /Users/amar.kulkarni/code/money-mentor-app/moneymentor
python -m app.evaluation.evaluator
```

## What Gets Logged to LangSmith?

For each query, LangSmith tracks:

### 1. **Input**
```json
{
  "query": "What is compound interest?",
  "k": 5
}
```

### 2. **Retrieved Context**
```json
{
  "contexts": [
    "Compound interest is calculated on...",
    "The formula for compound interest is...",
    ...
  ],
  "num_chunks": 5
}
```

### 3. **Generated Answer**
```json
{
  "answer": "Compound interest is interest calculated on both the principal...",
  "tool_used": "rag_tool",
  "sources": [...]
}
```

### 4. **Evaluation Metrics**
```json
{
  "faithfulness": 0.890,
  "answer_relevancy": 0.920,
  "context_precision": 0.850,
  "context_recall": 0.810
}
```

### 5. **Metadata**
```json
{
  "run_name": "MoneyMentor RAG Evaluation - 2025-10-18 23:30:00",
  "expected_answer": "Interest calculated on both...",
  "timestamp": "2025-10-18T23:30:00"
}
```

## Step 6: View Results in LangSmith Dashboard

1. Go to [smith.langchain.com](https://smith.langchain.com)
2. Select your **MoneyMentor** project
3. View the **Runs** tab

### Dashboard Features:

**📊 Overview**
- Total runs
- Success rate
- Average latency
- Token usage

**🔍 Individual Runs**
- Click any run to see:
  - Full trace (every LLM call)
  - Input/output
  - Timing breakdown
  - Metadata & tags

**📈 Metrics**
- View metrics over time
- Compare runs
- Identify trends

**🐛 Debugging**
- Filter by errors
- Search by query
- Compare expected vs. actual

## Step 7: Enhanced Evaluation with LangSmith SDK

For more advanced tracking, update `evaluator.py` to use LangSmith SDK:

```python
from langsmith import Client
from langsmith.run_helpers import traceable

# Initialize client
client = Client()

@traceable(name="MoneyMentor RAG Query")
def evaluate_query_with_trace(query: str, expected: str):
    """Evaluate with full LangSmith tracing."""
    
    # Get answer
    result = get_finance_answer(query)
    
    # Log metadata
    client.create_feedback(
        run_id=...,
        key="expected_answer",
        value=expected
    )
    
    return result
```

## Common LangSmith Use Cases

### 1. **Debugging Production Issues**
```python
# Search for failed runs
runs = client.list_runs(
    project_name="MoneyMentor",
    filter="error eq true"
)
```

### 2. **A/B Testing**
```python
# Compare different prompts
runs_v1 = client.list_runs(filter="metadata.version eq 'v1'")
runs_v2 = client.list_runs(filter="metadata.version eq 'v2'")
```

### 3. **Performance Monitoring**
```python
# Track latency over time
runs = client.list_runs(
    start_time=last_week,
    end_time=now
)
avg_latency = sum(r.latency for r in runs) / len(runs)
```

### 4. **User Feedback**
```python
# Add user ratings
client.create_feedback(
    run_id=run_id,
    key="user_rating",
    score=5,
    comment="Great answer!"
)
```

## Best Practices

### 1. **Organize with Tags**
```python
# Tag runs by feature
client.create_run(
    ...,
    tags=["rag", "financial-basics", "v1.0"]
)
```

### 2. **Use Metadata**
```python
# Add context
metadata = {
    "user_id": "user123",
    "session_id": "abc",
    "version": "1.0",
    "model": "gpt-4o-mini"
}
```

### 3. **Set Up Alerts**
1. Go to **Settings** → **Alerts**
2. Create alert for:
   - Error rate > 5%
   - Latency > 3 seconds
   - Daily runs < 10

### 4. **Export Data**
```python
# Download for analysis
runs = client.list_runs(project_name="MoneyMentor")
df = pd.DataFrame([r.dict() for r in runs])
df.to_csv("moneymentor_runs.csv")
```

## Troubleshooting

### "API key not valid"
```bash
# Check key format (should start with ls__)
echo $LANGCHAIN_API_KEY

# Regenerate key in LangSmith dashboard
```

### "Runs not appearing"
```bash
# Check tracing is enabled
echo $LANGCHAIN_TRACING_V2  # Should be "true"

# Check project name matches
echo $LANGCHAIN_PROJECT  # Should be "MoneyMentor"

# Restart backend to pick up new env vars
```

### "Connection errors"
```bash
# Test connectivity
curl https://api.smith.langchain.com/info

# Check firewall/proxy settings
```

## Cost & Limits

**Free Tier:**
- 5,000 traces/month
- 30-day retention
- 1 project

**Team Tier ($39/month):**
- 100,000 traces/month
- 90-day retention
- Unlimited projects
- Team collaboration

**Enterprise:**
- Unlimited traces
- Custom retention
- On-premise option
- SLA support

## Next Steps

1. ✅ Set up LangSmith account
2. ✅ Configure environment variables
3. ✅ Run first evaluation
4. ✅ View results in dashboard
5. 📊 Set up monitoring alerts
6. 📈 Track metrics over time
7. 🔄 Integrate into CI/CD

## Additional Resources

- 📚 [LangSmith Docs](https://docs.smith.langchain.com)
- 🎥 [Video Tutorials](https://www.youtube.com/langchain)
- 💬 [Discord Community](https://discord.gg/langchain)
- 📧 [Support](mailto:support@langchain.com)

---

Happy tracking! 🚀

