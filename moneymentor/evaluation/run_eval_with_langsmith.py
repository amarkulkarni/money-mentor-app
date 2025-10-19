#!/usr/bin/env python3
"""
Run MoneyMentor evaluation with LangSmith tracing.

This script properly wraps evaluation in LangSmith traceable functions.

Usage:
    python evaluation/run_eval_with_langsmith.py
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add app to path
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

# Load environment
from dotenv import load_dotenv
load_dotenv()

# Import LangSmith
try:
    from langsmith import Client
    from langsmith.run_helpers import traceable
    HAS_LANGSMITH = True
except ImportError:
    print("❌ LangSmith not installed. Run: pip install langsmith")
    HAS_LANGSMITH = False

from rag_pipeline import get_finance_answer


def load_golden_set(filepath: str):
    """Load test queries."""
    entries = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    return entries


@traceable(name="MoneyMentor_RAG_Evaluation", run_type="chain")
def evaluate_query(query: str, expected_answer: str):
    """
    Evaluate a single query with LangSmith tracing.
    
    This decorator ensures the entire evaluation is logged to LangSmith.
    """
    # Get answer from RAG pipeline
    result = get_finance_answer(query, k=5)
    
    # Extract data
    answer = result.get('answer', '')
    sources = result.get('sources', [])
    contexts = [s.get('text', '') for s in sources if s.get('text')]
    
    # Simple metrics (placeholder)
    answer_length = len(answer.split())
    num_sources = len(sources)
    
    return {
        "query": query,
        "expected_answer": expected_answer,
        "actual_answer": answer,
        "num_sources": num_sources,
        "answer_length": answer_length,
        "sources": sources,
        "contexts": contexts
    }


def main():
    """Run evaluation with LangSmith."""
    print("=" * 80)
    print("MoneyMentor Evaluation with LangSmith")
    print("=" * 80)
    print()
    
    # Check LangSmith configuration
    api_key = os.getenv("LANGCHAIN_API_KEY")
    tracing = os.getenv("LANGCHAIN_TRACING_V2")
    project = os.getenv("LANGCHAIN_PROJECT")
    
    print(f"🔑 API Key: {'✅ Set' if api_key else '❌ Not set'}")
    print(f"📊 Tracing: {'✅ Enabled' if tracing == 'true' else '❌ Disabled'}")
    print(f"📁 Project: {project or '❌ Not set'}")
    print()
    
    if not api_key or tracing != 'true':
        print("❌ LangSmith not properly configured!")
        print()
        print("Add to your .env file:")
        print("  LANGCHAIN_API_KEY=ls__your_key")
        print("  LANGCHAIN_TRACING_V2=true")
        print("  LANGCHAIN_PROJECT=MoneyMentor")
        sys.exit(1)
    
    # Load test set
    test_set_path = "evaluation/golden_set.jsonl"
    print(f"📂 Loading: {test_set_path}")
    golden_entries = load_golden_set(test_set_path)
    print(f"✅ Loaded {len(golden_entries)} queries")
    print()
    
    print("=" * 80)
    print("Running Evaluation (each run will appear in LangSmith)...")
    print("=" * 80)
    print()
    
    # Run evaluation
    results = []
    for i, entry in enumerate(golden_entries, 1):
        query = entry['query']
        expected = entry['expected_answer']
        
        print(f"[{i}/{len(golden_entries)}] {query[:60]}...")
        
        try:
            result = evaluate_query(query, expected)
            results.append(result)
            print(f"  ✅ Answer length: {result['answer_length']} words")
            print(f"  ✅ Sources: {result['num_sources']}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
            results.append({"query": query, "error": str(e)})
        
        print()
    
    # Save results
    output_path = "evaluation/eval_results_langsmith.json"
    with open(output_path, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_queries": len(golden_entries),
            "successful": sum(1 for r in results if 'error' not in r),
            "results": results
        }, f, indent=2)
    
    print("=" * 80)
    print(f"✅ Evaluation Complete!")
    print("=" * 80)
    print()
    print(f"📊 Results saved to: {output_path}")
    print()
    print("🔍 View in LangSmith:")
    print(f"   https://smith.langchain.com/projects/p/{project or 'MoneyMentor'}/traces")
    print()
    print("You should see {len(golden_entries)} runs in the dashboard! 🎉")


if __name__ == "__main__":
    if not HAS_LANGSMITH:
        sys.exit(1)
    main()

