# Semantic RAGAS Evaluation Results

**Dataset:** reasoning
**Method:** TF-IDF + Cosine Similarity
**Date:** 2025-10-20 22:16:03
**Queries:** 12

## Summary

| Retriever     |   Faithfulness |   Relevancy |   Precision |    Recall |   Queries | Dataset   | Δ Faithfulness   | Δ Relevancy   | Δ Precision   | Δ Recall   |
|:--------------|---------------:|------------:|------------:|----------:|----------:|:----------|:-----------------|:--------------|:--------------|:-----------|
| Base          |       0.138167 |    0.225917 |   0.0229167 | 0.0476667 |        12 | reasoning |                  |               |               |            |
| Hybrid+Rerank |       0.137417 |    0.231833 |   0.0229167 | 0.0476667 |        12 | reasoning | -0.1%            | +0.6%         | +0.0%         | +0.0%      |

## Key Findings

- **Faithfulness:** -0.1% improvement
- **Precision:** +0.0% improvement
- **Recall:** +0.0% improvement
- **Relevancy:** +0.6% improvement

## Notes

This evaluation uses TF-IDF vectorization with cosine similarity, which is lightweight and doesn't require PyTorch. While not as sophisticated as transformer-based embeddings, it provides reliable semantic similarity scoring.
