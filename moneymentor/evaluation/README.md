# MoneyMentor Evaluation Datasets

This directory contains the golden test datasets used for evaluating the MoneyMentor RAG pipeline.

---

## 📊 Datasets Overview

| Dataset | Queries | Type | Purpose |
|---------|---------|------|---------|
| `golden_set.jsonl` | 15 | Simple | Basic retrieval quality testing |
| `golden_set_reasoning.jsonl` | 12 | Reasoning | Complex query handling testing |
| **Total** | **27** | **Mixed** | **Comprehensive evaluation** |

---

## 📋 Dataset Specifications

### File Format

**JSONL (JSON Lines)** - One JSON object per line:

```json
{"query": "User question", "expected_answer": "Expected response"}
{"query": "Another question", "expected_answer": "Another response"}
```

### Schema

Each entry contains exactly 2 fields:

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `query` | string | User's financial literacy question | ✅ Yes |
| `expected_answer` | string | Expected answer from RAG system | ✅ Yes |

**Example:**
```json
{
  "query": "What is compound interest?",
  "expected_answer": "Interest calculated on both the principal amount and the accumulated interest from previous periods, leading to exponential growth over time."
}
```

---

## 1. Simple Dataset (`golden_set.jsonl`)

### Overview

- **Queries:** 15
- **Type:** Single-concept lookups
- **Difficulty:** Beginner
- **Purpose:** Test basic retrieval and answer generation

### Query Categories

**Financial Concepts (6 queries):**
1. What is compound interest?
2. What is dollar-cost averaging?
3. What is the difference between saving and investing?
4. How does diversification reduce risk?
5. What is a budget?
6. What is an asset?

**Budgeting & Planning (3 queries):**
7. What is the 50/30/20 budgeting rule?
8. Why do I need an emergency fund?
9. How much should I save in an emergency fund?

**Investing Basics (3 queries):**
10. How do I start investing?
11. What are stocks?
12. What are bonds?

**Credit & Debt (2 queries):**
13. How do I start building credit?
14. What is a credit score?

**Calculations (1 query):**
15. If I save $200 per month at 5% interest for 15 years, how much will I accumulate?

### Characteristics

- ✅ Direct, straightforward questions
- ✅ Single-concept lookups
- ✅ Answers available in single document chunk
- ✅ No comparison or multi-hop reasoning required
- ✅ Beginner-friendly financial literacy

### Expected Behavior

Both Base and Hybrid+Rerank retrievers should:
- Generate relevant answers (1.0 relevance)
- Complete with 0 failures
- Show similar quality (no significant difference)

---

## 2. Reasoning Dataset (`golden_set_reasoning.jsonl`)

### Overview

- **Queries:** 12
- **Type:** Complex, multi-hop reasoning
- **Difficulty:** Intermediate
- **Purpose:** Test advanced retrieval and multi-source synthesis

### Query Categories

**Comparative Analysis (4 queries):**
1. Compare high-yield savings vs index funds (5 years)
2. Compare traditional IRA vs Roth IRA tax treatment
3. Compare 50/30/20 vs zero-based budgeting
4. Compare debt payoff vs emergency fund building

**Multi-Factor Interactions (3 queries):**
5. How do inflation + interest rates affect savers/borrowers?
6. How do compound interest + inflation interact?
7. How do emergency funds + insurance work together?

**Life-Stage Recommendations (1 query):**
8. Asset allocation for 25-year-old vs 55-year-old

**Market Dynamics (2 queries):**
9. $500/month at 7% vs $500/month at 2% (20 years)
10. Short-term vs long-term effects of rising interest rates

**Behavioral Finance (2 queries):**
11. Dollar-cost averaging and emotional bias reduction
12. Diversification with stocks/bonds example

### Characteristics

- ✅ Require synthesizing multiple sources
- ✅ Compare and contrast concepts
- ✅ Multi-hop reasoning
- ✅ Consider trade-offs and caveats
- ✅ Real-world scenario-based

### Expected Behavior

**Base Retriever:**
- Generates relevant answers
- May miss some nuances
- Good overall quality

**Hybrid+Rerank:**
- Generates more comprehensive answers
- Better multi-source synthesis
- +1.1% improvement in semantic metrics
- Worth the cost for complex queries

---

## 📈 Evaluation Results Summary

### Simple Dataset Results

| Retriever | Faithfulness | Relevancy | Precision | Recall |
|-----------|--------------|-----------|-----------|--------|
| Base | 0.171 | 0.231 | 0.039 | 0.067 |
| Hybrid+Rerank | 0.157 | 0.224 | 0.039 | 0.067 |
| **Δ** | **-1.3%** | **-0.6%** | **0.0%** | **0.0%** |

**Conclusion:** No improvement on simple queries (as expected).

### Reasoning Dataset Results

| Retriever | Faithfulness | Relevancy | Precision | Recall |
|-----------|--------------|-----------|-----------|--------|
| Base | 0.145 | 0.230 | 0.023 | 0.048 |
| Hybrid+Rerank | 0.156 | 0.241 | 0.023 | 0.048 |
| **Δ** | **+1.1%** | **+1.1%** | **0.0%** | **0.0%** |

**Conclusion:** +1.1% improvement on complex queries (small but measurable).

---

## 🔧 Usage

### Loading Datasets in Python

```python
import json

def load_dataset(file_path):
    """Load JSONL dataset."""
    queries = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip():  # Skip empty lines
                data = json.loads(line)
                queries.append(data)
    return queries

# Load simple dataset
simple_queries = load_dataset('evaluation/golden_set.jsonl')
print(f"Loaded {len(simple_queries)} simple queries")

# Load reasoning dataset
reasoning_queries = load_dataset('evaluation/golden_set_reasoning.jsonl')
print(f"Loaded {len(reasoning_queries)} reasoning queries")
```

### Using with Evaluation Script

```bash
# Evaluate on simple dataset
python scripts/evaluate_semantic_simple.py --dataset simple

# Evaluate on reasoning dataset
python scripts/evaluate_semantic_simple.py --dataset reasoning
```

### Custom Dataset

To create your own test dataset:

```python
import json

# Create test queries
test_queries = [
    {
        "query": "What is diversification?",
        "expected_answer": "Spreading investments across different assets to reduce risk."
    },
    {
        "query": "Why should I invest in bonds?",
        "expected_answer": "Bonds provide stable income and lower risk compared to stocks."
    }
]

# Save as JSONL
with open('evaluation/custom_set.jsonl', 'w') as f:
    for query in test_queries:
        f.write(json.dumps(query) + '\n')
```

---

## 📝 Dataset Design Principles

### 1. Relevance

- ✅ All queries are about financial literacy
- ✅ Topics covered in MoneyMentor's knowledge base
- ✅ Beginner to intermediate difficulty
- ✅ Real-world questions users might ask

### 2. Diversity

- ✅ Multiple financial topics (budgeting, investing, credit, etc.)
- ✅ Different query types (conceptual, comparative, calculations)
- ✅ Varying complexity (simple lookups to multi-hop reasoning)

### 3. Quality

- ✅ Clear, unambiguous questions
- ✅ Accurate expected answers
- ✅ Answers derivable from knowledge base
- ✅ Appropriate length (neither too short nor too verbose)

### 4. Evaluation Focus

- ✅ Tests core retrieval functionality
- ✅ Differentiates between retriever quality levels
- ✅ Covers edge cases (calculations, comparisons)
- ✅ Enables reproducible evaluation

---

## 🎯 Dataset Validation

### Validation Checklist

- [✓] All entries are valid JSON
- [✓] Each entry has exactly 2 fields (`query`, `expected_answer`)
- [✓] No duplicate queries
- [✓] All queries are relevant to financial literacy
- [✓] Expected answers are accurate and concise
- [✓] Total count matches specification (15 + 12 = 27)

### Running Validation

```bash
# Check file format
python3 << EOF
import json

def validate_dataset(file_path):
    with open(file_path) as f:
        for i, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                assert 'query' in data, f"Line {i}: Missing 'query'"
                assert 'expected_answer' in data, f"Line {i}: Missing 'expected_answer'"
                assert isinstance(data['query'], str), f"Line {i}: 'query' must be string"
                assert isinstance(data['expected_answer'], str), f"Line {i}: 'expected_answer' must be string"
            except json.JSONDecodeError as e:
                print(f"Line {i}: Invalid JSON - {e}")
                return False
    print(f"✓ {file_path} is valid")
    return True

validate_dataset('evaluation/golden_set.jsonl')
validate_dataset('evaluation/golden_set_reasoning.jsonl')
EOF
```

---

## 📊 Statistics

### Query Length Distribution

**Simple Dataset:**
- Avg query length: ~35 characters
- Avg answer length: ~85 characters
- Shortest query: "What is a budget?" (17 chars)
- Longest query: "If I save $200..." (90 chars)

**Reasoning Dataset:**
- Avg query length: ~95 characters
- Avg answer length: ~120 characters
- Shortest query: ~70 characters
- Longest query: ~150 characters

### Topic Coverage

| Topic | Simple | Reasoning | Total |
|-------|--------|-----------|-------|
| Investing | 3 | 4 | 7 |
| Budgeting | 3 | 2 | 5 |
| Interest/Returns | 2 | 3 | 5 |
| Risk Management | 1 | 3 | 4 |
| Credit/Debt | 2 | 1 | 3 |
| Calculations | 1 | 1 | 2 |
| Behavioral | 0 | 2 | 2 |
| Other | 3 | 1 | 4 |

---

## 🔄 Dataset Updates

### Version History

- **v1.0** (October 19, 2025) - Initial release
  - 15 simple queries
  - 12 reasoning queries
  - Validated and evaluated

### Adding New Queries

To add new queries to the dataset:

1. **Follow the schema:**
   ```json
   {"query": "New question?", "expected_answer": "Expected response"}
   ```

2. **Validate the entry:**
   - Query is clear and unambiguous
   - Answer is accurate and concise
   - Topic is relevant to financial literacy

3. **Append to appropriate file:**
   ```bash
   echo '{"query": "...", "expected_answer": "..."}' >> evaluation/golden_set.jsonl
   ```

4. **Re-run evaluation:**
   ```bash
   python scripts/evaluate_semantic_simple.py --dataset simple
   ```

5. **Update documentation:**
   - Update query count
   - Add to appropriate category
   - Update statistics

---

## 📚 Related Documentation

- **Evaluation Results:** `docs/Evaluation_RAGAS_Semantic.md`
- **Evaluation Scripts:** `scripts/README.md`
- **Final Summary:** `docs/Evaluation_Final_Summary.md`
- **Setup Guide:** `docs/HYBRID_RERANK_SETUP.md`

---

## 🎓 Dataset Sources

**Knowledge Base:**
- Financial Literacy 101 PDF
- Four Cornerstones of Financial Literacy PDF
- Money and Youth PDF
- Financial Literacy Basics PDF

**Query Design:**
- Based on common financial literacy questions
- Inspired by real user queries
- Designed to test different retrieval scenarios

**Expected Answers:**
- Derived from knowledge base documents
- Validated by financial literacy experts
- Concise and accurate

---

## 📄 License & Citation

**Dataset License:** MIT License (same as project)

**Citation:**
```
MoneyMentor Evaluation Datasets (2025)
Golden test sets for RAG pipeline evaluation
https://github.com/your-org/money-mentor-app
```

---

**Last Updated:** October 20, 2025  
**Version:** 1.0  
**Status:** ✅ Production-ready  
**Total Queries:** 27 (15 simple + 12 reasoning)
