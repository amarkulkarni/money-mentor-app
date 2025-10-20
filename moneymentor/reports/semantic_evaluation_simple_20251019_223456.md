# Semantic RAGAS Evaluation Results

**Dataset:** simple
**Method:** TF-IDF + Cosine Similarity
**Date:** 2025-10-19 22:34:56
**Queries:** 15

## Summary

| Retriever     |   Faithfulness |   Relevancy |   Precision |    Recall |   Queries | Dataset   | Δ Faithfulness   | Δ Relevancy   | Δ Precision   | Δ Recall   |
|:--------------|---------------:|------------:|------------:|----------:|----------:|:----------|:-----------------|:--------------|:--------------|:-----------|
| Base          |       0.170533 |    0.230733 |      0.0392 | 0.0668667 |        15 | simple    |                  |               |               |            |
| Hybrid+Rerank |       0.157333 |    0.224267 |      0.0392 | 0.0668667 |        15 | simple    | -1.3%            | -0.6%         | +0.0%         | +0.0%      |

## Key Findings

- **Faithfulness:** -1.3% improvement
- **Precision:** +0.0% improvement
- **Recall:** +0.0% improvement
- **Relevancy:** -0.6% improvement

## Notes

This evaluation uses TF-IDF vectorization with cosine similarity, which is lightweight and doesn't require PyTorch. While not as sophisticated as transformer-based embeddings, it provides reliable semantic similarity scoring.
