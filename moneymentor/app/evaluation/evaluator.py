#!/usr/bin/env python3
"""
MoneyMentor RAG Evaluation with RAGAS Metrics

Evaluates the RAG pipeline using the RAGAS framework and logs to LangSmith.

Usage:
    python -m app.evaluation.evaluator
    
    Or from Python:
    from app.evaluation import evaluate_with_ragas
    results = evaluate_with_ragas("evaluation/golden_set.jsonl")
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Try relative import first, fall back to absolute
try:
    from ..rag_pipeline import get_finance_answer
except ImportError:
    # When run as script, use absolute import
    import sys
    import os
    # Add app directory to path
    app_dir = os.path.join(os.path.dirname(__file__), '..')
    if app_dir not in sys.path:
        sys.path.insert(0, app_dir)
    from rag_pipeline import get_finance_answer


def load_golden_set(filepath: str) -> List[Dict[str, str]]:
    """
    Load golden test set from JSONL file.
    
    Args:
        filepath: Path to golden_set.jsonl file
        
    Returns:
        List of dicts with 'query' and 'expected_answer' keys
    """
    entries = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    return entries


def score_faithfulness(generated: str, expected: str) -> float:
    """
    Score faithfulness: Does generated answer contain expected answer?
    
    Args:
        generated: Generated answer text
        expected: Expected/ground truth answer text
        
    Returns:
        1.0 if expected appears in generated (case-insensitive), else 0.0
    """
    return 1.0 if expected.lower() in generated.lower() else 0.0


def score_relevance(generated: str, query: str) -> float:
    """
    Score relevance: Does generated answer contain words from query?
    
    Args:
        generated: Generated answer text
        query: User query text
        
    Returns:
        1.0 if any query words appear in generated (case-insensitive), else 0.0
    """
    query_words = set(query.lower().split())
    generated_lower = generated.lower()
    return 1.0 if any(word in generated_lower for word in query_words) else 0.0


def score_context_precision(contexts: List[str], expected: str) -> float:
    """
    Score context precision: Does retrieved context contain expected answer?
    
    Args:
        contexts: List of retrieved context chunks
        expected: Expected/ground truth answer text
        
    Returns:
        1.0 if expected appears in any context (case-insensitive), else 0.0
    """
    context_text = " ".join(contexts).lower()
    return 1.0 if expected.lower() in context_text else 0.0


def score_context_recall(contexts: List[str], expected: str) -> float:
    """
    Score context recall: Does retrieved context contain expected answer?
    (For this simple implementation, same as precision)
    
    Args:
        contexts: List of retrieved context chunks
        expected: Expected/ground truth answer text
        
    Returns:
        1.0 if expected appears in any context (case-insensitive), else 0.0
    """
    context_text = " ".join(contexts).lower()
    return 1.0 if expected.lower() in context_text else 0.0


def compute_ragas_metrics(
    query: str,
    answer: str,
    expected_answer: str,
    contexts: List[str]
) -> Dict[str, float]:
    """
    Compute lightweight evaluation metrics using simple binary scoring.
    
    Compatible with GPT-nano for token efficiency.
    Each score is binary (1.0 or 0.0) for clear pass/fail evaluation.
    
    Args:
        query: User query
        answer: Generated answer
        expected_answer: Ground truth answer
        contexts: Retrieved context chunks
        
    Returns:
        Dict with metric scores (faithfulness, answer_relevancy, context_precision, context_recall)
    """
    try:
        return {
            "faithfulness": score_faithfulness(answer, expected_answer),
            "answer_relevancy": score_relevance(answer, query),
            "context_precision": score_context_precision(contexts, expected_answer),
            "context_recall": score_context_recall(contexts, expected_answer)
        }
        
    except Exception as e:
        print(f"⚠️  Warning: Could not compute metrics: {e}")
        return {
            "faithfulness": 0.0,
            "answer_relevancy": 0.0,
            "context_precision": 0.0,
            "context_recall": 0.0
        }


def log_to_langsmith(
    run_name: str,
    query: str,
    expected_answer: str,
    actual_answer: str,
    contexts: List[str],
    metrics: Dict[str, float]
) -> None:
    """
    Log evaluation results to LangSmith.
    
    Note: Requires LANGCHAIN_API_KEY environment variable.
    If not set, this function will silently skip logging.
    
    Args:
        run_name: Name for the LangSmith run
        query: User query
        expected_answer: Ground truth answer
        actual_answer: Generated answer
        contexts: Retrieved contexts
        metrics: RAGAS metrics dict
    """
    try:
        # Check if LangSmith is configured
        if not os.getenv("LANGCHAIN_API_KEY"):
            return  # Skip if not configured
        
        # Try to use LangSmith client
        try:
            from langsmith import Client
            
            client = Client()
            
            # Create a run with all evaluation data
            client.create_run(
                name=run_name,
                run_type="chain",
                inputs={"query": query, "expected_answer": expected_answer},
                outputs={"answer": actual_answer},
                extra={
                    "contexts": contexts,
                    "metrics": metrics,
                    "metadata": {
                        "evaluation_type": "RAGAS",
                        "retrieval_mode": mode,
                        "num_contexts": len(contexts),
                        "faithfulness": metrics.get("faithfulness", 0.0),
                        "answer_relevancy": metrics.get("answer_relevancy", 0.0),
                        "context_precision": metrics.get("context_precision", 0.0),
                        "context_recall": metrics.get("context_recall", 0.0)
                    }
                }
            )
            print(f"  📊 Logged to LangSmith: {run_name}")
            
        except ImportError:
            print(f"  ⚠️  LangSmith package not installed (pip install langsmith)")
        
    except Exception as e:
        print(f"  ⚠️  LangSmith logging failed: {e}")


def evaluate_with_ragas(test_set_path: str, mode: str = "base") -> Dict[str, Any]:
    """
    Evaluate MoneyMentor RAG pipeline with RAGAS metrics.
    
    Args:
        test_set_path: Path to golden test set JSONL file
        mode: Retrieval mode - "base" or "advanced" (default: "base")
        
    Returns:
        Dict containing:
        - results: List of per-query results
        - summary: Aggregate metrics
        - timestamp: Evaluation timestamp
        - mode: Retrieval mode used
    """
    print("=" * 80)
    print(f"MoneyMentor RAG Evaluation with RAGAS (Mode: {mode.upper()})")
    print("=" * 80)
    print()
    
    # Load golden set
    print(f"📂 Loading test set: {test_set_path}")
    golden_entries = load_golden_set(test_set_path)
    print(f"✅ Loaded {len(golden_entries)} test queries")
    print(f"🔧 Retrieval mode: {mode}")
    print()
    
    # Initialize results
    all_results = []
    run_name = f"MoneyMentor RAG Evaluation ({mode}) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    print("=" * 80)
    print("Running Evaluation...")
    print("=" * 80)
    print()
    
    # Evaluate each query
    for i, entry in enumerate(golden_entries, 1):
        query = entry['query']
        expected_answer = entry['expected_answer']
        
        print(f"[{i}/{len(golden_entries)}] {query[:70]}...")
        
        try:
            # Call RAG pipeline with specified mode
            rag_response = get_finance_answer(query, k=5, mode=mode)
            
            actual_answer = rag_response.get('answer', '')
            sources = rag_response.get('sources', [])
            
            # Extract context texts from sources
            contexts = [source.get('text', '') for source in sources if source.get('text')]
            
            # Compute RAGAS metrics
            metrics = compute_ragas_metrics(
                query=query,
                answer=actual_answer,
                expected_answer=expected_answer,
                contexts=contexts
            )
            
            # Log to LangSmith
            log_to_langsmith(
                run_name=run_name,
                query=query,
                expected_answer=expected_answer,
                actual_answer=actual_answer,
                contexts=contexts,
                metrics=metrics
            )
            
            # Store result
            result = {
                "query": query,
                "expected_answer": expected_answer,
                "actual_answer": actual_answer,
                "contexts": contexts,
                "sources": sources,
                "metrics": metrics
            }
            all_results.append(result)
            
            # Print metrics
            print(f"  ✓ Faithfulness: {metrics['faithfulness']:.3f}")
            print(f"  ✓ Relevancy: {metrics['answer_relevancy']:.3f}")
            print(f"  ✓ Precision: {metrics['context_precision']:.3f}")
            print(f"  ✓ Recall: {metrics['context_recall']:.3f}")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            result = {
                "query": query,
                "expected_answer": expected_answer,
                "actual_answer": "ERROR",
                "contexts": [],
                "sources": [],
                "metrics": {
                    "faithfulness": 0.0,
                    "answer_relevancy": 0.0,
                    "context_precision": 0.0,
                    "context_recall": 0.0
                },
                "error": str(e)
            }
            all_results.append(result)
        
        print()
    
    # Compute summary statistics
    successful_results = [r for r in all_results if r.get('actual_answer') != 'ERROR']
    
    if successful_results:
        avg_metrics = {
            "avg_faithfulness": sum(r['metrics']['faithfulness'] for r in successful_results) / len(successful_results),
            "avg_answer_relevancy": sum(r['metrics']['answer_relevancy'] for r in successful_results) / len(successful_results),
            "avg_context_precision": sum(r['metrics']['context_precision'] for r in successful_results) / len(successful_results),
            "avg_context_recall": sum(r['metrics']['context_recall'] for r in successful_results) / len(successful_results)
        }
    else:
        avg_metrics = {
            "avg_faithfulness": 0.0,
            "avg_answer_relevancy": 0.0,
            "avg_context_precision": 0.0,
            "avg_context_recall": 0.0
        }
    
    # Create final results object
    evaluation_results = {
        "timestamp": datetime.now().isoformat(),
        "test_set": test_set_path,
        "mode": mode,
        "total_queries": len(golden_entries),
        "successful": len(successful_results),
        "failed": len(golden_entries) - len(successful_results),
        "summary": avg_metrics,
        "results": all_results
    }
    
    # Save results to JSON
    output_path = "evaluation/eval_results.json"
    with open(output_path, 'w') as f:
        json.dump(evaluation_results, f, indent=2)
    print(f"💾 Results saved to: {output_path}")
    print()
    
    # Print Markdown table
    print("=" * 80)
    print("Results Summary (Markdown Table)")
    print("=" * 80)
    print()
    print("| # | Query | Faithfulness | Relevance | Precision | Recall |")
    print("|---|-------|--------------|-----------|-----------|--------|")
    
    for i, result in enumerate(all_results, 1):
        query_short = result['query'][:40] + "..." if len(result['query']) > 40 else result['query']
        m = result['metrics']
        print(f"| {i} | {query_short} | {m['faithfulness']:.3f} | {m['answer_relevancy']:.3f} | {m['context_precision']:.3f} | {m['context_recall']:.3f} |")
    
    print()
    print("**Average Metrics:**")
    print(f"- Faithfulness: {avg_metrics['avg_faithfulness']:.3f}")
    print(f"- Answer Relevancy: {avg_metrics['avg_answer_relevancy']:.3f}")
    print(f"- Context Precision: {avg_metrics['avg_context_precision']:.3f}")
    print(f"- Context Recall: {avg_metrics['avg_context_recall']:.3f}")
    print()
    
    print("=" * 80)
    print("Evaluation Complete! 🎉")
    print("=" * 80)
    
    return evaluation_results


if __name__ == "__main__":
    """
    CLI entrypoint for running evaluation.
    
    Usage:
        python -m app.evaluation.evaluator [mode] [dataset]
        
    Arguments:
        mode: "base" or "advanced" (default: "base")
        dataset: Path to test set jsonl file (default: "evaluation/golden_set.jsonl")
        
    Examples:
        # Simple queries with base retriever
        python -m app.evaluation.evaluator base
        
        # Simple queries with advanced retriever
        python -m app.evaluation.evaluator advanced
        
        # Reasoning queries with base retriever
        python -m app.evaluation.evaluator base evaluation/golden_set_reasoning.jsonl
        
        # Reasoning queries with advanced retriever
        python -m app.evaluation.evaluator advanced evaluation/golden_set_reasoning.jsonl
    """
    import sys
    
    # Default values
    test_set_path = "evaluation/golden_set.jsonl"
    mode = "base"
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        mode = sys.argv[1]  # First arg is mode
    if len(sys.argv) > 2:
        test_set_path = sys.argv[2]  # Second arg is test set path
    
    # Validate mode
    if mode not in ["base", "advanced"]:
        print(f"❌ Error: Invalid mode '{mode}'. Must be 'base' or 'advanced'")
        print()
        print("Usage:")
        print("  python -m app.evaluation.evaluator [mode] [dataset]")
        print()
        print("Examples:")
        print("  python -m app.evaluation.evaluator base")
        print("  python -m app.evaluation.evaluator advanced")
        print("  python -m app.evaluation.evaluator base evaluation/golden_set.jsonl")
        print("  python -m app.evaluation.evaluator advanced evaluation/golden_set_reasoning.jsonl")
        sys.exit(1)
    
    # Check if file exists
    if not os.path.exists(test_set_path):
        print(f"❌ Error: Test set file not found: {test_set_path}")
        print()
        print("Usage:")
        print("  python -m app.evaluation.evaluator [mode] [dataset]")
        print()
        print("Available datasets:")
        print("  - evaluation/golden_set.jsonl (15 simple queries)")
        print("  - evaluation/golden_set_reasoning.jsonl (12 complex queries)")
        print()
        print("Example:")
        print("  python -m app.evaluation.evaluator advanced evaluation/golden_set_reasoning.jsonl")
        sys.exit(1)
    
    # Detect dataset type for better logging
    dataset_name = "simple" if "golden_set.jsonl" in test_set_path else "reasoning"
    print(f"📊 Dataset: {dataset_name} ({test_set_path})")
    print(f"🔧 Mode: {mode}")
    print()
    
    # Run evaluation
    try:
        results = evaluate_with_ragas(test_set_path, mode=mode)
        sys.exit(0)
    except Exception as e:
        print(f"❌ Evaluation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

