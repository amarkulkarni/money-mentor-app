#!/usr/bin/env python3
"""
Validate MoneyMentor evaluation datasets.

Checks:
- JSON format validity
- Required fields present
- Data types correct
- No duplicates
- Reasonable lengths
"""

import json
import sys
from pathlib import Path


def validate_dataset(file_path: str, expected_count: int) -> bool:
    """
    Validate a JSONL dataset file.
    
    Args:
        file_path: Path to JSONL file
        expected_count: Expected number of queries
        
    Returns:
        True if valid, False otherwise
    """
    print(f"\n{'='*80}")
    print(f"Validating: {file_path}")
    print(f"{'='*80}\n")
    
    if not Path(file_path).exists():
        print(f"❌ Error: File not found: {file_path}")
        return False
    
    queries = []
    query_texts = set()
    errors = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            # Skip empty lines
            if not line.strip():
                continue
            
            # Parse JSON
            try:
                data = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"Line {line_num}: Invalid JSON - {e}")
                continue
            
            # Check required fields
            if 'query' not in data:
                errors.append(f"Line {line_num}: Missing 'query' field")
                continue
            if 'expected_answer' not in data:
                errors.append(f"Line {line_num}: Missing 'expected_answer' field")
                continue
            
            # Check data types
            if not isinstance(data['query'], str):
                errors.append(f"Line {line_num}: 'query' must be a string")
                continue
            if not isinstance(data['expected_answer'], str):
                errors.append(f"Line {line_num}: 'expected_answer' must be a string")
                continue
            
            # Check for extra fields (warning only)
            extra_fields = set(data.keys()) - {'query', 'expected_answer'}
            if extra_fields:
                print(f"⚠️  Line {line_num}: Extra fields found: {extra_fields}")
            
            # Check lengths
            if len(data['query']) < 5:
                errors.append(f"Line {line_num}: Query too short ({len(data['query'])} chars)")
            if len(data['expected_answer']) < 10:
                errors.append(f"Line {line_num}: Answer too short ({len(data['expected_answer'])} chars)")
            
            # Check for duplicates
            if data['query'] in query_texts:
                errors.append(f"Line {line_num}: Duplicate query: {data['query'][:50]}...")
            
            query_texts.add(data['query'])
            queries.append(data)
    
    # Print errors
    if errors:
        print("❌ Validation errors found:\n")
        for error in errors:
            print(f"  {error}")
        print()
        return False
    
    # Check count
    actual_count = len(queries)
    if actual_count != expected_count:
        print(f"⚠️  Warning: Expected {expected_count} queries, found {actual_count}")
    
    # Print summary
    print(f"✅ Validation successful!")
    print(f"\nStatistics:")
    print(f"  Total queries: {actual_count}")
    print(f"  Unique queries: {len(query_texts)}")
    
    # Query length stats
    query_lengths = [len(q['query']) for q in queries]
    answer_lengths = [len(q['expected_answer']) for q in queries]
    
    print(f"\nQuery lengths:")
    print(f"  Min: {min(query_lengths)} chars")
    print(f"  Max: {max(query_lengths)} chars")
    print(f"  Avg: {sum(query_lengths) / len(query_lengths):.1f} chars")
    
    print(f"\nAnswer lengths:")
    print(f"  Min: {min(answer_lengths)} chars")
    print(f"  Max: {max(answer_lengths)} chars")
    print(f"  Avg: {sum(answer_lengths) / len(answer_lengths):.1f} chars")
    
    # Sample queries
    print(f"\nSample queries:")
    for i, query in enumerate(queries[:3], 1):
        print(f"  {i}. {query['query'][:60]}...")
    
    return True


def main():
    """Validate all datasets."""
    print("\n" + "="*80)
    print("MONEYMENTOR DATASET VALIDATION")
    print("="*80)
    
    datasets = [
        ('evaluation/golden_set.jsonl', 15, 'Simple queries'),
        ('evaluation/golden_set_reasoning.jsonl', 12, 'Reasoning queries'),
    ]
    
    all_valid = True
    
    for file_path, expected_count, description in datasets:
        print(f"\n{description}:")
        valid = validate_dataset(file_path, expected_count)
        if not valid:
            all_valid = False
    
    # Final summary
    print("\n" + "="*80)
    if all_valid:
        print("✅ ALL DATASETS VALID!")
        print("="*80)
        print("\nDatasets are ready for:")
        print("  - Evaluation scripts")
        print("  - Repository submission")
        print("  - Reproducibility")
        print()
        sys.exit(0)
    else:
        print("❌ VALIDATION FAILED")
        print("="*80)
        print("\nPlease fix the errors above and try again.\n")
        sys.exit(1)


if __name__ == '__main__':
    main()

