#!/usr/bin/env python3
"""
MoneyMentor - Simplified Semantic RAGAS Evaluation (No Torch Required)

Uses sklearn's TF-IDF vectorization for semantic similarity instead of sentence-transformers.
This avoids the need for PyTorch while still providing semantic similarity scoring.

Usage:
    python scripts/evaluate_semantic_simple.py
    python scripts/evaluate_semantic_simple.py --dataset reasoning
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import argparse

# Add directories to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "app"))

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import dependencies
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import pandas as pd
    import numpy as np
    from dotenv import load_dotenv
    
    # Load RAG pipeline
    from app.rag_pipeline import get_finance_answer
    
    # LangSmith tracking
    try:
        from langsmith import Client
        langsmith_client = Client()
        HAS_LANGSMITH = True
    except ImportError:
        HAS_LANGSMITH = False
        langsmith_client = None
        logger.warning("LangSmith not available")
        
except ImportError as e:
    logger.error(f"Missing dependency: {e}")
    logger.error("Install with: pip install scikit-learn pandas numpy")
    sys.exit(1)

# Load environment
load_dotenv()

# Initialize TF-IDF vectorizer for semantic similarity
logger.info("Initializing TF-IDF vectorizer for semantic similarity...")
vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 3),
    stop_words='english'
)
logger.info("✅ TF-IDF vectorizer ready\n")


def compute_semantic_similarity(text1: str, text2: str) -> float:
    """
    Compute semantic similarity using TF-IDF vectors and cosine similarity.
    
    Returns:
        Float between 0.0 and 1.0
    """
    try:
        vectors = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        # Ensure positive value (cosine can be negative)
        return max(0.0, min(1.0, similarity))
    except Exception as e:
        logger.warning(f"Similarity computation failed: {e}")
        return 0.0


def score_semantic_faithfulness(generated: str, expected: str, contexts: List[str]) -> float:
    """
    Semantic faithfulness: How well does the generated answer match the expected answer?
    """
    return compute_semantic_similarity(generated, expected)


def score_semantic_relevancy(generated: str, query: str) -> float:
    """
    Semantic relevancy: How well does the answer address the query?
    """
    return compute_semantic_similarity(generated, query)


def score_semantic_precision(contexts: List[str], expected: str) -> float:
    """
    Semantic precision: How relevant are the retrieved contexts?
    
    Average similarity of contexts to expected answer.
    """
    if not contexts:
        return 0.0
    
    similarities = [compute_semantic_similarity(ctx, expected) for ctx in contexts]
    return sum(similarities) / len(similarities)


def score_semantic_recall(contexts: List[str], expected: str) -> float:
    """
    Semantic recall: Do the contexts contain information needed for the answer?
    
    Maximum similarity among contexts (best context relevance).
    """
    if not contexts:
        return 0.0
    
    similarities = [compute_semantic_similarity(ctx, expected) for ctx in contexts]
    return max(similarities)


def load_test_dataset(dataset_path: str) -> List[Dict[str, str]]:
    """Load test queries from JSONL file."""
    queries = []
    with open(dataset_path, 'r') as f:
        for line in f:
            if line.strip():
                data = json.loads(line)
                queries.append({
                    "query": data["query"],
                    "expected_answer": data["expected_answer"]
                })
    return queries


def evaluate_retriever(
    mode: str,
    queries: List[Dict[str, str]],
    dataset_name: str = "simple"
) -> List[Dict[str, Any]]:
    """
    Evaluate a retriever with semantic metrics.
    
    Args:
        mode: "base" or "advanced"
        queries: List of query dicts with query and expected_answer
        dataset_name: Name of dataset for logging
        
    Returns:
        List of result dicts with metrics
    """
    results = []
    
    logger.info(f"\n{'='*80}")
    logger.info(f"Evaluating {mode.upper()} retriever on {dataset_name} dataset")
    logger.info(f"{'='*80}\n")
    
    for i, query_data in enumerate(queries, 1):
        query = query_data["query"]
        expected = query_data["expected_answer"]
        
        logger.info(f"[{i}/{len(queries)}] {query[:60]}...")
        
        try:
            # Get answer with contexts
            response = get_finance_answer(
                query=query,
                mode=mode,
                return_context=True,
                k=5
            )
            
            generated = response["answer"]
            contexts = response.get("contexts", [])
            
            # Compute semantic metrics
            faithfulness = score_semantic_faithfulness(generated, expected, contexts)
            relevancy = score_semantic_relevancy(generated, query)
            precision = score_semantic_precision(contexts, expected)
            recall = score_semantic_recall(contexts, expected)
            
            result = {
                "query": query,
                "expected_answer": expected,
                "generated_answer": generated,
                "num_contexts": len(contexts),
                "faithfulness": round(faithfulness, 3),
                "relevancy": round(relevancy, 3),
                "precision": round(precision, 3),
                "recall": round(recall, 3),
                "mode": mode,
                "dataset": dataset_name
            }
            
            results.append(result)
            
            logger.info(f"  ✓ Faithfulness: {faithfulness:.3f}")
            logger.info(f"  ✓ Relevancy: {relevancy:.3f}")
            logger.info(f"  ✓ Precision: {precision:.3f}")
            logger.info(f"  ✓ Recall: {recall:.3f}\n")
            
            # Log to LangSmith
            if HAS_LANGSMITH and langsmith_client:
                try:
                    run = langsmith_client.create_run(
                        name=f"Semantic_Eval_{mode}_{dataset_name}",
                        run_type="evaluation",
                        inputs={"query": query, "mode": mode, "dataset": dataset_name},
                        outputs=result,
                        tags=[
                            "moneymentor",
                            "semantic_evaluation_tfidf",
                            f"retriever={mode}",
                            f"dataset={dataset_name}"
                        ]
                    )
                    # Close run immediately
                    langsmith_client.update_run(run.id, end_time=datetime.now().isoformat())
                except Exception as e:
                    logger.warning(f"LangSmith logging failed: {e}")
                    
        except Exception as e:
            logger.error(f"  ❌ Error processing query: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    return results


def generate_comparison_report(
    base_results: List[Dict[str, Any]],
    hybrid_results: List[Dict[str, Any]],
    dataset_name: str
) -> pd.DataFrame:
    """Generate comparison DataFrame and summary statistics."""
    
    # Calculate averages
    base_avg = {
        "Retriever": "Base",
        "Faithfulness": sum(r["faithfulness"] for r in base_results) / len(base_results),
        "Relevancy": sum(r["relevancy"] for r in base_results) / len(base_results),
        "Precision": sum(r["precision"] for r in base_results) / len(base_results),
        "Recall": sum(r["recall"] for r in base_results) / len(base_results),
        "Queries": len(base_results),
        "Dataset": dataset_name
    }
    
    hybrid_avg = {
        "Retriever": "Hybrid+Rerank",
        "Faithfulness": sum(r["faithfulness"] for r in hybrid_results) / len(hybrid_results),
        "Relevancy": sum(r["relevancy"] for r in hybrid_results) / len(hybrid_results),
        "Precision": sum(r["precision"] for r in hybrid_results) / len(hybrid_results),
        "Recall": sum(r["recall"] for r in hybrid_results) / len(hybrid_results),
        "Queries": len(hybrid_results),
        "Dataset": dataset_name
    }
    
    # Create DataFrame
    df = pd.DataFrame([base_avg, hybrid_avg])
    
    # Add improvement columns
    df["Δ Faithfulness"] = df["Faithfulness"].diff()
    df["Δ Relevancy"] = df["Relevancy"].diff()
    df["Δ Precision"] = df["Precision"].diff()
    df["Δ Recall"] = df["Recall"].diff()
    
    # Format percentages
    for col in ["Δ Faithfulness", "Δ Relevancy", "Δ Precision", "Δ Recall"]:
        df[col] = df[col].apply(lambda x: f"{x:+.1%}" if pd.notna(x) else "")
    
    return df


def save_results(
    base_results: List[Dict[str, Any]],
    hybrid_results: List[Dict[str, Any]],
    comparison_df: pd.DataFrame,
    dataset_name: str
):
    """Save all results to files."""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save detailed results
    detailed_results = {
        "evaluation_date": datetime.now().isoformat(),
        "dataset": dataset_name,
        "method": "TF-IDF + Cosine Similarity",
        "base_retriever": base_results,
        "hybrid_retriever": hybrid_results,
        "summary": comparison_df.to_dict(orient="records")
    }
    
    results_path = f"reports/semantic_evaluation_{dataset_name}_{timestamp}.json"
    with open(results_path, 'w') as f:
        json.dump(detailed_results, f, indent=2)
    logger.info(f"✅ Detailed results saved: {results_path}")
    
    # Save comparison CSV
    csv_path = f"reports/semantic_comparison_{dataset_name}_{timestamp}.csv"
    comparison_df.to_csv(csv_path, index=False)
    logger.info(f"✅ Comparison CSV saved: {csv_path}")
    
    # Save markdown report
    md_path = f"reports/semantic_evaluation_{dataset_name}_{timestamp}.md"
    with open(md_path, 'w') as f:
        f.write(f"# Semantic RAGAS Evaluation Results\n\n")
        f.write(f"**Dataset:** {dataset_name}\n")
        f.write(f"**Method:** TF-IDF + Cosine Similarity\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Queries:** {len(base_results)}\n\n")
        f.write(f"## Summary\n\n")
        f.write(comparison_df.to_markdown(index=False))
        f.write(f"\n\n## Key Findings\n\n")
        
        # Extract improvements
        hybrid_row = comparison_df.iloc[1]
        f.write(f"- **Faithfulness:** {hybrid_row['Δ Faithfulness']} improvement\n")
        f.write(f"- **Precision:** {hybrid_row['Δ Precision']} improvement\n")
        f.write(f"- **Recall:** {hybrid_row['Δ Recall']} improvement\n")
        f.write(f"- **Relevancy:** {hybrid_row['Δ Relevancy']} improvement\n\n")
        f.write(f"## Notes\n\n")
        f.write(f"This evaluation uses TF-IDF vectorization with cosine similarity, ")
        f.write(f"which is lightweight and doesn't require PyTorch. While not as sophisticated ")
        f.write(f"as transformer-based embeddings, it provides reliable semantic similarity scoring.\n")
        
    logger.info(f"✅ Markdown report saved: {md_path}")


def main():
    """Main evaluation pipeline."""
    parser = argparse.ArgumentParser(description="Semantic RAGAS evaluation (TF-IDF)")
    parser.add_argument(
        "--dataset",
        default="simple",
        choices=["simple", "reasoning"],
        help="Dataset to evaluate (simple or reasoning)"
    )
    args = parser.parse_args()
    
    # Determine dataset path
    if args.dataset == "simple":
        dataset_path = "evaluation/golden_set.jsonl"
        dataset_name = "simple"
    else:
        dataset_path = "evaluation/golden_set_reasoning.jsonl"
        dataset_name = "reasoning"
    
    logger.info(f"\n{'='*80}")
    logger.info(f"SEMANTIC RAGAS EVALUATION (TF-IDF)")
    logger.info(f"{'='*80}")
    logger.info(f"Dataset: {dataset_name}")
    logger.info(f"Path: {dataset_path}")
    logger.info(f"Method: TF-IDF + Cosine Similarity")
    logger.info(f"{'='*80}\n")
    
    # Load test queries
    queries = load_test_dataset(dataset_path)
    logger.info(f"✅ Loaded {len(queries)} test queries\n")
    
    # Evaluate Base retriever
    base_results = evaluate_retriever("base", queries, dataset_name)
    
    # Evaluate Hybrid+Rerank retriever
    hybrid_results = evaluate_retriever("advanced", queries, dataset_name)
    
    # Generate comparison
    logger.info(f"\n{'='*80}")
    logger.info(f"GENERATING COMPARISON REPORT")
    logger.info(f"{'='*80}\n")
    
    comparison_df = generate_comparison_report(base_results, hybrid_results, dataset_name)
    
    # Print results
    print("\n" + "="*80)
    print("SEMANTIC RAGAS EVALUATION RESULTS")
    print("="*80 + "\n")
    print(comparison_df.to_string(index=False))
    print("\n" + "="*80 + "\n")
    
    # Save results
    save_results(base_results, hybrid_results, comparison_df, dataset_name)
    
    logger.info("\n✅ Semantic evaluation complete!")
    logger.info(f"Check reports/ directory for detailed results\n")


if __name__ == "__main__":
    main()

