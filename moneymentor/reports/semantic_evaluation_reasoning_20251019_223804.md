# Semantic RAGAS Evaluation Results

**Dataset:** reasoning
**Method:** TF-IDF + Cosine Similarity
**Date:** 2025-10-19 22:38:05
**Queries:** 12

## Summary

| Retriever     |   Faithfulness |   Relevancy |   Precision |    Recall |   Queries | Dataset   | Δ Faithfulness   | Δ Relevancy   | Δ Precision   | Δ Recall   |
|:--------------|---------------:|------------:|------------:|----------:|----------:|:----------|:-----------------|:--------------|:--------------|:-----------|
| Base          |       0.145083 |    0.229667 |   0.0229167 | 0.0476667 |        12 | reasoning |                  |               |               |            |
| Hybrid+Rerank |       0.156167 |    0.24075  |   0.0229167 | 0.0476667 |        12 | reasoning | +1.1%            | +1.1%         | +0.0%         | +0.0%      |

## Key Findings

- **Faithfulness:** +1.1% improvement
- **Precision:** +0.0% improvement
- **Recall:** +0.0% improvement
- **Relevancy:** +1.1% improvement

## Notes

This evaluation uses TF-IDF vectorization with cosine similarity, which is lightweight and doesn't require PyTorch. While not as sophisticated as transformer-based embeddings, it provides reliable semantic similarity scoring.
