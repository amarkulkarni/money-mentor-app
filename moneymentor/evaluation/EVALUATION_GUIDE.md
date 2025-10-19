# MoneyMentor Evaluation Guide

This guide explains how to evaluate MoneyMentor's RAG pipeline using the RAGAS framework.

## Quick Start

### 1. Run Evaluation

```bash
# Make sure backend is running
cd app && python -m uvicorn main:app --reload --port 8000

# In another terminal, run evaluation
cd /Users/amar.kulkarni/code/money-mentor-app/moneymentor
python -m app.evaluation.evaluator
```

### 2. View Results

The evaluation will:
- Test all 15 queries from `golden_set.jsonl`
- Compute RAGAS metrics for each
- Print a markdown table with results
- Save detailed results to `evaluation/eval_results.json`

## Metrics Explained

### Faithfulness (0.0 - 1.0)
**What it measures:** Does the answer align with the retrieved context?

- **High score (>0.8):** Answer is well-grounded in source documents
- **Low score (<0.5):** Answer may contain hallucinations or unsupported claims

**Example:**
- Query: "What is compound interest?"
- Good: "Interest calculated on principal and accumulated interest" ✓
- Bad: "A new cryptocurrency investment strategy" ✗

### Answer Relevancy (0.0 - 1.0)
**What it measures:** Does the answer address the user's query?

- **High score (>0.85):** Answer directly addresses the question
- **Low score (<0.6):** Answer is off-topic or incomplete

**Example:**
- Query: "How do I build credit?"
- Good: "Get a secured credit card and pay on time" ✓
- Bad: "Credit is important for financial health" (not actionable) ✗

### Context Precision (0.0 - 1.0)
**What it measures:** Quality of retrieved context chunks

- **High score (>0.8):** Retrieved docs are highly relevant
- **Low score (<0.5):** Many irrelevant chunks retrieved

**Example:**
- Query: "What is a 401(k)?"
- Good context: Passages about retirement accounts ✓
- Bad context: Random finance definitions ✗

### Context Recall (0.0 - 1.0)
**What it measures:** Did we retrieve all relevant information?

- **High score (>0.75):** All key facts are in retrieved context
- **Low score (<0.5):** Missing important information

**Example:**
- Expected: "401(k) is employer-sponsored, tax-deferred, with matching"
- Good recall: Context mentions all three aspects ✓
- Poor recall: Context only mentions tax benefits ✗

## Target Performance

| Metric | Target | Good | Needs Work |
|--------|--------|------|------------|
| Faithfulness | >0.8 | >0.85 | <0.7 |
| Answer Relevancy | >0.85 | >0.9 | <0.75 |
| Context Precision | >0.8 | >0.85 | <0.7 |
| Context Recall | >0.75 | >0.85 | <0.65 |

## Output Files

### `evaluation/eval_results.json`
Complete evaluation results including:
```json
{
  "timestamp": "2025-10-18T23:30:00",
  "total_queries": 15,
  "successful": 15,
  "summary": {
    "avg_faithfulness": 0.856,
    "avg_answer_relevancy": 0.892,
    "avg_context_precision": 0.834,
    "avg_context_recall": 0.789
  },
  "results": [...]
}
```

### Markdown Table (Console Output)
```
| # | Query | Faithfulness | Relevance | Precision | Recall |
|---|-------|--------------|-----------|-----------|--------|
| 1 | What is compound interest? | 0.890 | 0.920 | 0.850 | 0.810 |
| 2 | What is the 50/30/20 rule? | 0.870 | 0.900 | 0.820 | 0.790 |
...
```

## Using with LangSmith (Optional)

To enable LangSmith tracking:

```bash
# Add to your .env file
export LANGCHAIN_API_KEY="your-api-key"
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_PROJECT="MoneyMentor"
```

Then run evaluation as normal. Results will appear in your LangSmith dashboard.

## Programmatic Usage

```python
from app.evaluation import evaluate_with_ragas

# Run evaluation
results = evaluate_with_ragas("evaluation/golden_set.jsonl")

# Access metrics
print(f"Average Faithfulness: {results['summary']['avg_faithfulness']}")

# Inspect individual results
for result in results['results']:
    print(f"Query: {result['query']}")
    print(f"Metrics: {result['metrics']}")
```

## Improving Low Scores

### Low Faithfulness
**Problem:** Model is hallucinating or not grounding answers in context

**Solutions:**
1. Improve prompt engineering (emphasize "use only provided context")
2. Increase chunk overlap in text splitter
3. Add citation requirements to prompt
4. Fine-tune embedding model on domain data

### Low Answer Relevancy
**Problem:** Model not directly addressing the question

**Solutions:**
1. Improve query understanding
2. Add few-shot examples to prompt
3. Use query expansion/reformulation
4. Implement answer validation step

### Low Context Precision
**Problem:** Retrieving too many irrelevant chunks

**Solutions:**
1. Improve embedding model quality
2. Increase similarity threshold
3. Use hybrid search (keyword + semantic)
4. Implement re-ranking step

### Low Context Recall
**Problem:** Missing relevant information

**Solutions:**
1. Increase `k` (number of chunks retrieved)
2. Reduce chunk size for better granularity
3. Implement multi-query retrieval
4. Add more diverse content to knowledge base

## Custom Test Sets

To create your own test set:

```bash
# Create new JSONL file
cat > evaluation/my_test_set.jsonl << 'EOF'
{"query": "My custom question?", "expected_answer": "Expected answer"}
{"query": "Another question?", "expected_answer": "Another answer"}
EOF

# Run evaluation
python -m app.evaluation.evaluator evaluation/my_test_set.jsonl
```

## Continuous Evaluation

For CI/CD integration:

```bash
# Run as part of your pipeline
python -m app.evaluation.evaluator

# Check exit code
if [ $? -eq 0 ]; then
    echo "✅ Evaluation passed"
else
    echo "❌ Evaluation failed"
    exit 1
fi
```

## Troubleshooting

### "Module not found" errors
```bash
# Install evaluation dependencies
cd /Users/amar.kulkarni/code/money-mentor-app/moneymentor
pip install ragas langsmith requests
```

### "Connection refused" errors
```bash
# Make sure backend is running
cd app && python -m uvicorn main:app --reload --port 8000
```

### Low scores across the board
1. Check if PDFs are properly indexed
2. Verify Qdrant is running and populated
3. Test individual queries manually in chat UI
4. Review `eval_results.json` for error messages

## Next Steps

1. **Baseline Metrics:** Run evaluation to establish baseline
2. **Iterate:** Make improvements to RAG pipeline
3. **Re-evaluate:** Run again to measure improvements
4. **Monitor:** Set up automated evaluation in CI/CD
5. **LangSmith:** Enable tracking for production monitoring

---

Happy evaluating! 🎯

