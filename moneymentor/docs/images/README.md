# Evaluation Charts

This directory contains visualizations of the semantic RAGAS evaluation results comparing Base vs Hybrid+Rerank retrievers.

## Charts

### 1. Simple Dataset Results
**File:** `semantic_eval_simple.png`

Side-by-side comparison of Base vs Hybrid+Rerank on 15 simple queries.

**Embedding in Markdown:**
```markdown
![Simple Dataset Results](images/semantic_eval_simple.png)
```

### 2. Reasoning Dataset Results
**File:** `semantic_eval_reasoning.png`

Side-by-side comparison of Base vs Hybrid+Rerank on 12 complex reasoning queries.

**Embedding in Markdown:**
```markdown
![Reasoning Dataset Results](images/semantic_eval_reasoning.png)
```

### 3. Improvement Analysis
**File:** `semantic_eval_improvement.png`

Percentage improvement of Hybrid+Rerank over Base for both datasets.

**Embedding in Markdown:**
```markdown
![Improvement Analysis](images/semantic_eval_improvement.png)
```

## Regenerating Charts

To regenerate the charts with updated data:

```bash
python scripts/generate_charts.py
```

**Update data in:** `scripts/generate_charts.py`
- Edit `SIMPLE_DATA` and `REASONING_DATA` dictionaries
- Run the script to regenerate all charts

## Chart Specifications

- **Format:** PNG (300 DPI)
- **Color Palette:**
  - Base Retriever: Soft Blue (#4A90E2)
  - Hybrid+Rerank: Emerald Green (#50C878)
  - Grid: Light Gray (#E0E0E0)
  - Text: Dark Blue-Gray (#2C3E50)
- **Size:** 
  - Comparison charts: 12" × 7"
  - Improvement chart: 10" × 7"
- **Style:** Modern, professional, not glaring

## Chart Details

### Metrics Shown
- **Faithfulness:** How well the generated answer matches the expected answer
- **Relevancy:** How well the answer addresses the query
- **Precision:** How relevant the retrieved contexts are
- **Recall:** Whether contexts contain information needed for the answer

### Key Insights from Charts

**Simple Dataset:**
- No improvement from Hybrid+Rerank
- Both retrievers perform similarly
- Simple queries don't benefit from advanced retrieval

**Reasoning Dataset:**
- +1.1% improvement in Faithfulness
- +1.1% improvement in Relevancy
- Complex queries benefit slightly from Hybrid+Rerank

**Overall:**
- Improvement is modest (+1.1%)
- Cost increase is significant (12.5×)
- ROI depends on business context

