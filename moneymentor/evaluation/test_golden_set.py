#!/usr/bin/env python3
"""
Test script to evaluate MoneyMentor responses against the golden set.

Usage:
    python evaluation/test_golden_set.py
"""

import json
import requests
import sys
from typing import List, Dict

API_URL = "http://localhost:8000/api/chat"
GOLDEN_SET_PATH = "evaluation/golden_set.jsonl"


def load_golden_set(filepath: str) -> List[Dict]:
    """Load golden set from JSONL file."""
    entries = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    return entries


def query_moneymentor(question: str) -> Dict:
    """Send query to MoneyMentor API."""
    try:
        response = requests.post(
            API_URL,
            json={"question": question, "k": 5},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e), "answer": "ERROR"}


def main():
    """Run evaluation on golden set."""
    print("=" * 80)
    print("MoneyMentor Golden Set Evaluation")
    print("=" * 80)
    print()
    
    # Load golden set
    print(f"📂 Loading golden set from: {GOLDEN_SET_PATH}")
    golden_entries = load_golden_set(GOLDEN_SET_PATH)
    print(f"✅ Loaded {len(golden_entries)} test queries")
    print()
    
    # Check API availability
    try:
        health = requests.get("http://localhost:8000/api/health", timeout=5)
        if health.status_code != 200:
            print("❌ MoneyMentor API is not available!")
            print("   Please start the backend: cd app && python -m uvicorn main:app --reload")
            sys.exit(1)
        print("✅ MoneyMentor API is running")
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        print("   Please start the backend: cd app && python -m uvicorn main:app --reload")
        sys.exit(1)
    
    print()
    print("=" * 80)
    print("Running Queries...")
    print("=" * 80)
    print()
    
    results = []
    for i, entry in enumerate(golden_entries, 1):
        query = entry['query']
        expected = entry['expected_answer']
        
        print(f"[{i}/{len(golden_entries)}] {query}")
        print(f"Expected: {expected[:100]}...")
        
        # Query API
        response = query_moneymentor(query)
        
        if "error" in response:
            print(f"❌ Error: {response['error']}")
            results.append({
                "query": query,
                "expected": expected,
                "actual": "ERROR",
                "passed": False
            })
        else:
            actual = response.get('answer', 'No answer')
            tool = response.get('tool', 'unknown')
            sources_count = len(response.get('sources', []))
            
            print(f"Actual: {actual[:100]}...")
            print(f"Tool: {tool} | Sources: {sources_count}")
            
            results.append({
                "query": query,
                "expected": expected,
                "actual": actual,
                "tool": tool,
                "sources": sources_count,
                "passed": None  # Manual evaluation needed
            })
        
        print("-" * 80)
        print()
    
    # Summary
    print("=" * 80)
    print("Evaluation Complete!")
    print("=" * 80)
    print(f"Total queries: {len(results)}")
    print(f"Successful responses: {sum(1 for r in results if r.get('actual') != 'ERROR')}")
    print()
    print("💡 For detailed metrics, integrate with RAGAS:")
    print("   from app.evaluation import evaluate_with_ragas")
    print("   results = evaluate_with_ragas('evaluation/golden_set.jsonl')")
    print()


if __name__ == "__main__":
    main()

