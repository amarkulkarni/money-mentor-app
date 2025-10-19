"""
MoneyMentor - Evaluation Module

This module provides evaluation utilities for the RAG pipeline using RAGAS metrics.
RAGAS (Retrieval-Augmented Generation Assessment) helps evaluate:
- Context relevance
- Answer faithfulness
- Answer relevance
- Context recall

Usage:
    python -m app.evaluation --test-set data/test_set.jsonl
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


def evaluate_with_ragas(test_set_path: str) -> Dict[str, float]:
    """
    Evaluate RAG pipeline using RAGAS metrics.
    
    This is a placeholder that will be implemented in Phase 2.
    The function will load a test set and compute RAGAS metrics including:
    - Context Precision: How relevant are retrieved contexts?
    - Context Recall: Are all relevant contexts retrieved?
    - Faithfulness: Is the answer faithful to the context?
    - Answer Relevance: How relevant is the answer to the question?
    
    Args:
        test_set_path: Path to JSONL file containing test questions and ground truth
        
    Returns:
        Dictionary with metric scores
        
    Test Set Format (JSONL):
        {"question": "What is compound interest?", "ground_truth": "...", "contexts": [...]}
        {"question": "How to create a budget?", "ground_truth": "...", "contexts": [...]}
    
    Example:
        >>> results = evaluate_with_ragas("data/test_set.jsonl")
        >>> print(f"Faithfulness: {results['faithfulness']:.3f}")
    """
    test_set_file = Path(test_set_path)
    
    logger.info("=" * 70)
    logger.info("RAGAS Evaluation - Placeholder")
    logger.info("=" * 70)
    
    if not test_set_file.exists():
        logger.warning(f"⚠️  Test set not found: {test_set_path}")
        logger.info("To create a test set, create a JSONL file with this format:")
        logger.info('{"question": "What is compound interest?", "ground_truth": "..."}')
        logger.info('{"question": "How to budget?", "ground_truth": "..."}')
        return {
            'status': 'no_test_set',
            'message': 'Test set file not found'
        }
    
    # Load test set
    try:
        test_cases = []
        with open(test_set_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line:
                    try:
                        test_cases.append(json.loads(line))
                    except json.JSONDecodeError as e:
                        logger.error(f"Invalid JSON on line {line_num}: {e}")
        
        logger.info(f"✅ Loaded {len(test_cases)} test cases from {test_set_path}")
        
        # Display what would be evaluated
        logger.info("")
        logger.info("📊 RAGAS Metrics to be computed:")
        logger.info("  1. Context Precision - Relevance of retrieved chunks")
        logger.info("  2. Context Recall - Coverage of relevant information")
        logger.info("  3. Faithfulness - Answer grounded in context")
        logger.info("  4. Answer Relevance - Answer addresses the question")
        logger.info("")
        
        logger.info("📝 Sample Test Cases:")
        for i, test_case in enumerate(test_cases[:3], 1):
            question = test_case.get('question', 'N/A')
            logger.info(f"  {i}. {question[:60]}...")
        
        if len(test_cases) > 3:
            logger.info(f"  ... and {len(test_cases) - 3} more")
        
        logger.info("")
        logger.info("🚧 Implementation Status: PLACEHOLDER")
        logger.info("   This will be implemented in Phase 2 with:")
        logger.info("   - RAGAS library integration")
        logger.info("   - Automated metric computation")
        logger.info("   - Results visualization")
        logger.info("   - Performance benchmarking")
        logger.info("")
        logger.info("=" * 70)
        
        return {
            'status': 'placeholder',
            'test_cases_loaded': len(test_cases),
            'message': 'RAGAS evaluation not yet implemented',
            'next_steps': [
                'Install ragas: pip install ragas',
                'Implement metric computation',
                'Add automated evaluation pipeline'
            ]
        }
        
    except Exception as e:
        logger.error(f"❌ Error loading test set: {e}")
        return {
            'status': 'error',
            'message': str(e)
        }


def create_sample_test_set(output_path: str = "data/sample_test_set.jsonl") -> None:
    """
    Create a sample test set for evaluation.
    
    Args:
        output_path: Where to save the sample test set
    """
    sample_cases = [
        {
            "question": "What is compound interest?",
            "ground_truth": "Compound interest is interest calculated on the initial principal and also on the accumulated interest from previous periods.",
            "contexts": []
        },
        {
            "question": "How should I create a budget?",
            "ground_truth": "To create a budget: 1) Track your income, 2) List all expenses, 3) Categorize spending, 4) Set limits for each category, 5) Monitor and adjust regularly.",
            "contexts": []
        },
        {
            "question": "What is the 50/30/20 rule?",
            "ground_truth": "The 50/30/20 rule suggests allocating 50% of income to needs, 30% to wants, and 20% to savings and debt repayment.",
            "contexts": []
        }
    ]
    
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for case in sample_cases:
            f.write(json.dumps(case) + '\n')
    
    logger.info(f"✅ Created sample test set: {output_path}")
    logger.info(f"   Contains {len(sample_cases)} test cases")


if __name__ == "__main__":
    """
    CLI entrypoint for evaluation
    
    Usage:
        # Evaluate with existing test set
        python -m app.evaluation --test-set data/test_set.jsonl
        
        # Create sample test set
        python -m app.evaluation --create-sample
    """
    import argparse
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )
    
    parser = argparse.ArgumentParser(
        description="Evaluate MoneyMentor RAG pipeline with RAGAS"
    )
    parser.add_argument(
        '--test-set',
        default='data/test_set.jsonl',
        help='Path to test set JSONL file'
    )
    parser.add_argument(
        '--create-sample',
        action='store_true',
        help='Create a sample test set'
    )
    
    args = parser.parse_args()
    
    if args.create_sample:
        create_sample_test_set()
    else:
        results = evaluate_with_ragas(args.test_set)
        
        if results['status'] == 'placeholder':
            print("\n" + "=" * 70)
            print("Next Steps:")
            print("=" * 70)
            for step in results['next_steps']:
                print(f"  • {step}")
            print("=" * 70)

