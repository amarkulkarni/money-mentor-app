# MoneyMentor Evaluation Dataset

This directory contains evaluation datasets for testing MoneyMentor's RAG pipeline, calculator, and multi-tool agent performance.

## Golden Set (`golden_set.jsonl`)

A curated dataset of 15 sample queries with expected answers for evaluating MoneyMentor's responses.

### Query Types

**Conceptual Questions (RAG Tool)** - 8 queries
- Compound interest definition
- Budgeting rules (50/30/20)
- Emergency funds
- Saving vs. investing
- Credit scores
- Good vs. bad debt
- Inflation effects
- Diversification
- Dollar-cost averaging
- Building credit

**Calculation Questions (Calculator Tool)** - 3 queries
- Monthly investment: $500/month at 7% for 20 years
- Lump sum: $10,000 at 6% for 10 years
- Monthly savings: $200/month at 5% for 15 years

**Advisory Questions (Multi-Tool)** - 2 queries
- 401(k) retirement accounts
- Debt payoff vs. retirement savings prioritization

### Format

Each line is a JSON object with:
```json
{
  "query": "User question",
  "expected_answer": "Accurate answer from knowledge base or calculation"
}
```

### Usage

For RAGAS evaluation:
```python
from app.evaluation import evaluate_with_ragas

results = evaluate_with_ragas("evaluation/golden_set.jsonl")
```

For manual testing:
```bash
# Test a single query
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is compound interest?"}'

# Test all queries
python evaluation/run_evaluation.py
```

### Expected Performance

- **RAG Questions**: Should retrieve relevant context from financial literacy PDFs
- **Calculator Questions**: Should use finance_calculator_tool for accurate computations
- **Multi-Tool Questions**: Should combine RAG + Tavily or RAG + Calculator appropriately

### Metrics

When evaluating with RAGAS:
- **Faithfulness**: Answer accuracy vs. source documents
- **Answer Relevancy**: Response relevance to query
- **Context Recall**: Coverage of ground truth
- **Context Precision**: Quality of retrieved context

Target scores: 
- Faithfulness: > 0.8
- Answer Relevancy: > 0.85
- Context Recall: > 0.75
- Context Precision: > 0.80

## Adding New Test Cases

To add new queries:
1. Add a new line to `golden_set.jsonl`
2. Ensure proper JSON formatting
3. Verify query tests a specific tool or scenario
4. Run evaluation to establish baseline

Example:
```json
{"query": "What is a mutual fund?", "expected_answer": "An investment vehicle that pools money from multiple investors to purchase a diversified portfolio of stocks, bonds, or other securities, managed by professional fund managers."}
```

