#!/usr/bin/env python3
"""
Generate bar charts for semantic evaluation results.

Creates side-by-side bar charts comparing Base vs Hybrid+Rerank retrievers.
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Set style for modern, professional charts
plt.style.use('seaborn-v0_8-darkgrid')

# Modern color palette (not glaring)
COLORS = {
    'base': '#4A90E2',        # Soft blue
    'hybrid': '#50C878',      # Emerald green
    'grid': '#E0E0E0',        # Light gray
    'text': '#2C3E50'         # Dark blue-gray
}

# Data from semantic evaluation results
SIMPLE_DATA = {
    'Base': {
        'Faithfulness': 0.171,
        'Relevancy': 0.231,
        'Precision': 0.039,
        'Recall': 0.067
    },
    'Hybrid+Rerank': {
        'Faithfulness': 0.157,
        'Relevancy': 0.224,
        'Precision': 0.039,
        'Recall': 0.067
    }
}

REASONING_DATA = {
    'Base': {
        'Faithfulness': 0.145,
        'Relevancy': 0.230,
        'Precision': 0.023,
        'Recall': 0.048
    },
    'Hybrid+Rerank': {
        'Faithfulness': 0.156,
        'Relevancy': 0.241,
        'Precision': 0.023,
        'Recall': 0.048
    }
}


def create_comparison_chart(data, title, filename, dataset_info):
    """
    Create a side-by-side bar chart comparing Base vs Hybrid+Rerank.
    
    Args:
        data: Dictionary with 'Base' and 'Hybrid+Rerank' metrics
        title: Chart title
        filename: Output filename
        dataset_info: Description of dataset (e.g., "15 queries")
    """
    metrics = list(data['Base'].keys())
    base_values = list(data['Base'].values())
    hybrid_values = list(data['Hybrid+Rerank'].values())
    
    # Set up the figure
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Bar positions
    x = np.arange(len(metrics))
    width = 0.35
    
    # Create bars
    bars1 = ax.bar(x - width/2, base_values, width, label='Base Retriever',
                   color=COLORS['base'], alpha=0.9, edgecolor='white', linewidth=1.5)
    bars2 = ax.bar(x + width/2, hybrid_values, width, label='Hybrid+Rerank',
                   color=COLORS['hybrid'], alpha=0.9, edgecolor='white', linewidth=1.5)
    
    # Customize the chart
    ax.set_ylabel('Score', fontsize=13, fontweight='bold', color=COLORS['text'])
    ax.set_xlabel('Metrics', fontsize=13, fontweight='bold', color=COLORS['text'])
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20, color=COLORS['text'])
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=11, color=COLORS['text'])
    
    # Add dataset info as subtitle
    ax.text(0.5, 1.02, dataset_info, transform=ax.transAxes,
            fontsize=11, color='gray', ha='center', style='italic')
    
    # Customize y-axis
    ax.set_ylim(0, max(max(base_values), max(hybrid_values)) * 1.2)
    ax.yaxis.grid(True, linestyle='--', alpha=0.3, color=COLORS['grid'])
    ax.set_axisbelow(True)
    
    # Add value labels on bars
    def add_value_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.3f}',
                   ha='center', va='bottom', fontsize=9,
                   color=COLORS['text'], fontweight='bold')
    
    add_value_labels(bars1)
    add_value_labels(bars2)
    
    # Legend
    ax.legend(loc='upper right', frameon=True, shadow=True, fontsize=11,
              fancybox=True, framealpha=0.95)
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['grid'])
    ax.spines['bottom'].set_color(COLORS['grid'])
    
    # Tight layout
    plt.tight_layout()
    
    # Save
    output_path = Path('docs/images') / filename
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Saved: {output_path}")
    
    plt.close()


def create_delta_chart(simple_data, reasoning_data):
    """
    Create a chart showing improvement deltas for Faithfulness and Relevancy.
    """
    # Calculate deltas
    simple_faith_delta = (simple_data['Hybrid+Rerank']['Faithfulness'] - 
                          simple_data['Base']['Faithfulness']) / simple_data['Base']['Faithfulness'] * 100
    simple_rel_delta = (simple_data['Hybrid+Rerank']['Relevancy'] - 
                        simple_data['Base']['Relevancy']) / simple_data['Base']['Relevancy'] * 100
    
    reasoning_faith_delta = (reasoning_data['Hybrid+Rerank']['Faithfulness'] - 
                             reasoning_data['Base']['Faithfulness']) / reasoning_data['Base']['Faithfulness'] * 100
    reasoning_rel_delta = (reasoning_data['Hybrid+Rerank']['Relevancy'] - 
                           reasoning_data['Base']['Relevancy']) / reasoning_data['Base']['Relevancy'] * 100
    
    # Data
    metrics = ['Faithfulness', 'Relevancy']
    simple_deltas = [simple_faith_delta, simple_rel_delta]
    reasoning_deltas = [reasoning_faith_delta, reasoning_rel_delta]
    
    # Set up the figure
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Bar positions
    x = np.arange(len(metrics))
    width = 0.35
    
    # Create bars with conditional coloring
    bars1 = ax.bar(x - width/2, simple_deltas, width, label='Simple Queries (15)',
                   color=[COLORS['hybrid'] if v > 0 else '#E74C3C' for v in simple_deltas],
                   alpha=0.9, edgecolor='white', linewidth=1.5)
    bars2 = ax.bar(x + width/2, reasoning_deltas, width, label='Reasoning Queries (12)',
                   color=[COLORS['hybrid'] if v > 0 else '#E74C3C' for v in reasoning_deltas],
                   alpha=0.9, edgecolor='white', linewidth=1.5)
    
    # Customize the chart
    ax.set_ylabel('% Improvement (Hybrid+Rerank vs Base)', fontsize=12, 
                  fontweight='bold', color=COLORS['text'])
    ax.set_xlabel('Metrics', fontsize=12, fontweight='bold', color=COLORS['text'])
    ax.set_title('Hybrid+Rerank Performance Improvement', fontsize=16, 
                 fontweight='bold', pad=20, color=COLORS['text'])
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=11, color=COLORS['text'])
    
    # Add subtitle
    ax.text(0.5, 1.02, 'Percentage improvement over Base retriever', 
            transform=ax.transAxes, fontsize=11, color='gray', ha='center', style='italic')
    
    # Zero line
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8, alpha=0.5)
    
    # Grid
    ax.yaxis.grid(True, linestyle='--', alpha=0.3, color=COLORS['grid'])
    ax.set_axisbelow(True)
    
    # Add value labels
    def add_value_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:+.1f}%',
                   ha='center', va='bottom' if height > 0 else 'top',
                   fontsize=10, color=COLORS['text'], fontweight='bold')
    
    add_value_labels(bars1)
    add_value_labels(bars2)
    
    # Legend
    ax.legend(loc='upper left', frameon=True, shadow=True, fontsize=10,
              fancybox=True, framealpha=0.95)
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['grid'])
    ax.spines['bottom'].set_color(COLORS['grid'])
    
    # Tight layout
    plt.tight_layout()
    
    # Save
    output_path = Path('docs/images') / 'semantic_eval_improvement.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Saved: {output_path}")
    
    plt.close()


def main():
    """Generate all evaluation charts."""
    print("\n" + "="*80)
    print("📊 GENERATING SEMANTIC EVALUATION CHARTS")
    print("="*80 + "\n")
    
    # Simple dataset chart
    create_comparison_chart(
        data=SIMPLE_DATA,
        title='Semantic Evaluation Results: Simple Dataset',
        filename='semantic_eval_simple.png',
        dataset_info='15 single-concept queries (e.g., "What is compound interest?")'
    )
    
    # Reasoning dataset chart
    create_comparison_chart(
        data=REASONING_DATA,
        title='Semantic Evaluation Results: Reasoning Dataset',
        filename='semantic_eval_reasoning.png',
        dataset_info='12 complex queries (e.g., "Compare traditional IRA vs Roth IRA...")'
    )
    
    # Improvement delta chart
    create_delta_chart(SIMPLE_DATA, REASONING_DATA)
    
    print("\n" + "="*80)
    print("✅ ALL CHARTS GENERATED SUCCESSFULLY!")
    print("="*80)
    print("\nFiles created:")
    print("  - docs/images/semantic_eval_simple.png")
    print("  - docs/images/semantic_eval_reasoning.png")
    print("  - docs/images/semantic_eval_improvement.png")
    print("\nReady to embed in markdown documentation! 🎉\n")


if __name__ == '__main__':
    main()

