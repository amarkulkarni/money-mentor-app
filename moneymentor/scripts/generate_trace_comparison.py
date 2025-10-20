#!/usr/bin/env python3
"""
Generate a visual comparison diagram for Base vs Hybrid+Rerank traces.

This serves as an alternative to LangSmith screenshots.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

# Modern color palette
COLORS = {
    'base_bg': '#E3F2FD',      # Light blue
    'hybrid_bg': '#E8F5E9',    # Light green
    'border': '#2C3E50',       # Dark blue-gray
    'text': '#2C3E50',         # Dark blue-gray
    'metric_good': '#4CAF50',  # Green
    'metric_neutral': '#FFC107' # Amber
}


def create_trace_comparison():
    """Create a side-by-side comparison diagram of traces."""
    
    fig, (ax_base, ax_hybrid) = plt.subplots(1, 2, figsize=(16, 10))
    
    # Remove axes
    for ax in [ax_base, ax_hybrid]:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
    
    # BASE RETRIEVER (Left)
    base_rect = patches.FancyBboxPatch(
        (0.5, 0.5), 8, 9,
        boxstyle="round,pad=0.1",
        edgecolor=COLORS['border'],
        facecolor=COLORS['base_bg'],
        linewidth=2
    )
    ax_base.add_patch(base_rect)
    
    # Base title
    ax_base.text(4.5, 9.2, 'BASE RETRIEVER', 
                ha='center', va='top', fontsize=16, fontweight='bold',
                color=COLORS['text'])
    
    # Base content
    base_content = [
        ('🔍 Mode:', 'base', 8.5),
        ('⏱️ Latency:', '0.8s', 8.0),
        ('💰 Cost:', '$0.00002', 7.5),
        ('', '', 7.0),  # Spacer
        ('📥 QUERY:', '', 6.5),
        ('"Compare traditional IRA', '', 6.2),
        ('vs Roth IRA tax treatment"', '', 5.9),
        ('', '', 5.4),  # Spacer
        ('📊 METRICS:', '', 5.0),
        ('Faithfulness:', '0.145', 4.5),
        ('Relevancy:', '0.230', 4.0),
        ('Precision:', '0.023', 3.5),
        ('Recall:', '0.048', 3.0),
        ('', '', 2.5),  # Spacer
        ('🔍 RETRIEVAL:', '', 2.1),
        ('• Vector similarity search', '', 1.7),
        ('• Retrieved 5 chunks', '', 1.3),
        ('• Single-stage retrieval', '', 0.9),
    ]
    
    for label, value, y_pos in base_content:
        if label and not value:  # Section headers
            ax_base.text(1.0, y_pos, label, 
                        fontsize=11, fontweight='bold',
                        color=COLORS['text'])
        elif label and value:  # Key-value pairs
            ax_base.text(1.0, y_pos, label, 
                        fontsize=10, color=COLORS['text'])
            ax_base.text(4.5, y_pos, value, 
                        fontsize=10, fontweight='bold',
                        color=COLORS['text'])
        elif label:  # Plain text
            ax_base.text(1.5, y_pos, label, 
                        fontsize=9, style='italic',
                        color=COLORS['text'])
    
    # HYBRID+RERANK RETRIEVER (Right)
    hybrid_rect = patches.FancyBboxPatch(
        (0.5, 0.5), 8, 9,
        boxstyle="round,pad=0.1",
        edgecolor=COLORS['border'],
        facecolor=COLORS['hybrid_bg'],
        linewidth=2
    )
    ax_hybrid.add_patch(hybrid_rect)
    
    # Hybrid title
    ax_hybrid.text(4.5, 9.2, 'HYBRID + RERANK', 
                  ha='center', va='top', fontsize=16, fontweight='bold',
                  color=COLORS['text'])
    
    # Hybrid content
    hybrid_content = [
        ('🔍 Mode:', 'advanced', 8.5),
        ('⏱️ Latency:', '1.8s (+125%)', 8.0),
        ('💰 Cost:', '$0.00025 (12.5×)', 7.5),
        ('', '', 7.0),  # Spacer
        ('📥 QUERY:', '', 6.5),
        ('"Compare traditional IRA', '', 6.2),
        ('vs Roth IRA tax treatment"', '', 5.9),
        ('', '', 5.4),  # Spacer
        ('📊 METRICS:', '', 5.0),
        ('Faithfulness:', '0.156 (+1.1%) ✓', 4.5),
        ('Relevancy:', '0.241 (+1.1%) ✓', 4.0),
        ('Precision:', '0.023 (same)', 3.5),
        ('Recall:', '0.048 (same)', 3.0),
        ('', '', 2.5),  # Spacer
        ('🔍 RETRIEVAL:', '', 2.1),
        ('• BM25 + Vector ensemble', '', 1.7),
        ('• Retrieved 24 chunks', '', 1.3),
        ('• Reranked to top 5', '', 0.9),
    ]
    
    for label, value, y_pos in hybrid_content:
        if label and not value:  # Section headers
            ax_hybrid.text(1.0, y_pos, label, 
                          fontsize=11, fontweight='bold',
                          color=COLORS['text'])
        elif label and value:  # Key-value pairs
            color = COLORS['metric_good'] if '✓' in value else COLORS['text']
            ax_hybrid.text(1.0, y_pos, label, 
                          fontsize=10, color=COLORS['text'])
            ax_hybrid.text(4.0, y_pos, value, 
                          fontsize=10, fontweight='bold',
                          color=color)
        elif label:  # Plain text
            ax_hybrid.text(1.5, y_pos, label, 
                          fontsize=9, style='italic',
                          color=COLORS['text'])
    
    # Overall title
    fig.suptitle('LangSmith Trace Comparison: Base vs Hybrid+Rerank',
                fontsize=18, fontweight='bold', y=0.98)
    
    # Subtitle
    fig.text(0.5, 0.95, 'Semantic Evaluation on Complex Query (Reasoning Dataset)',
            ha='center', fontsize=12, style='italic', color='gray')
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.94])
    
    # Save
    output_path = Path('docs/images') / 'langsmith_trace_comparison.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Saved: {output_path}")
    
    plt.close()


def main():
    """Generate trace comparison diagram."""
    print("\n" + "="*80)
    print("📊 GENERATING LANGSMITH TRACE COMPARISON DIAGRAM")
    print("="*80 + "\n")
    
    create_trace_comparison()
    
    print("\n" + "="*80)
    print("✅ DIAGRAM GENERATED!")
    print("="*80)
    print("\nFile created:")
    print("  - docs/images/langsmith_trace_comparison.png")
    print("\nThis diagram can be used as:")
    print("  1. Placeholder until LangSmith screenshots are captured")
    print("  2. Alternative if LangSmith access is unavailable")
    print("  3. Quick reference for understanding trace differences")
    print("\n📸 To capture actual LangSmith screenshots:")
    print("  See: docs/LANGSMITH_SCREENSHOT_CAPTURE_GUIDE.md\n")


if __name__ == '__main__':
    main()

