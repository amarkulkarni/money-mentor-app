# MoneyMentor Evaluation Scripts

This directory contains all scripts for evaluating and visualizing the MoneyMentor RAG pipeline performance.

---

## 📋 Table of Contents

1. [Scripts Overview](#scripts-overview)
2. [Quick Start](#quick-start)
3. [Script Details](#script-details)
4. [Dependencies](#dependencies)
5. [Output Files](#output-files)
6. [Troubleshooting](#troubleshooting)

---

## Scripts Overview

| Script | Purpose | Input | Output | Runtime |
|--------|---------|-------|--------|---------|
| `evaluate_semantic_simple.py` | Semantic RAGAS evaluation | JSONL datasets | JSON, CSV, MD reports | ~10 min |
| `evaluate_semantic_retrievers.py` | Semantic evaluation (with PyTorch) | JSONL datasets | JSON, CSV, MD reports | ~10 min |
| `generate_charts.py` | Generate bar charts | Hardcoded data | PNG charts | ~5 sec |
| `generate_trace_comparison.py` | Generate trace diagram | Hardcoded data | PNG diagram | ~3 sec |

---

## Quick Start

### 1. Setup Environment

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify environment
python --version  # Should be Python 3.8+
```

### 2. Run Semantic Evaluation

```bash
# Evaluate on simple dataset (15 queries)
python scripts/evaluate_semantic_simple.py --dataset simple

# Evaluate on reasoning dataset (12 queries)
python scripts/evaluate_semantic_simple.py --dataset reasoning

# Both evaluations
python scripts/evaluate_semantic_simple.py --dataset simple
python scripts/evaluate_semantic_simple.py --dataset reasoning
```

### 3. Generate Visualizations

```bash
# Generate bar charts
python scripts/generate_charts.py

# Generate trace comparison
python scripts/generate_trace_comparison.py
```

---

## Script Details

### 1. `evaluate_semantic_simple.py` ⭐ **Recommended**

**Purpose:** Semantic RAGAS evaluation using TF-IDF + cosine similarity (no PyTorch required).

**Features:**
- ✅ No PyTorch dependency (uses scikit-learn)
- ✅ Evaluates both Base and Hybrid+Rerank retrievers
- ✅ Supports simple and reasoning datasets
- ✅ Generates JSON, CSV, and Markdown reports
- ✅ Optional LangSmith logging

**Usage:**
```bash
# Basic usage
python scripts/evaluate_semantic_simple.py

# Specify dataset
python scripts/evaluate_semantic_simple.py --dataset simple
python scripts/evaluate_semantic_simple.py --dataset reasoning

# Help
python scripts/evaluate_semantic_simple.py --help
```

**Arguments:**
- `--dataset`: Choice of `simple` or `reasoning` (default: `simple`)

**Input Files:**
- `evaluation/golden_set.jsonl` - Simple queries (15)
- `evaluation/golden_set_reasoning.jsonl` - Reasoning queries (12)

**Output Files:**
- `reports/semantic_evaluation_{dataset}_{timestamp}.json` - Detailed results
- `reports/semantic_comparison_{dataset}_{timestamp}.csv` - Comparison table
- `reports/semantic_evaluation_{dataset}_{timestamp}.md` - Markdown report

**Environment Variables:**
- `OPENAI_API_KEY` - Required for RAG pipeline
- `QDRANT_URL` - Qdrant connection (default: http://localhost:6333)
- `QDRANT_API_KEY` - Optional
- `COHERE_API_KEY` - Required for Hybrid+Rerank mode
- `LANGCHAIN_API_KEY` - Optional for LangSmith tracking
- `LANGCHAIN_TRACING_V2` - Optional (set to `true` for tracking)

**Example Output:**
```
================================================================================
SEMANTIC RAGAS EVALUATION RESULTS
================================================================================
    Retriever  Faithfulness  Relevancy  Precision   Recall  Queries Dataset
         Base         0.171      0.231      0.039    0.067       15  simple
Hybrid+Rerank         0.157      0.224      0.039    0.067       15  simple
```

---

### 2. `evaluate_semantic_retrievers.py` ⚠️ **Requires PyTorch**

**Purpose:** Semantic RAGAS evaluation using SentenceTransformers (more sophisticated, but requires PyTorch).

**Features:**
- ✅ Uses transformer-based embeddings (better semantic similarity)
- ✅ More accurate than TF-IDF
- ⚠️ Requires PyTorch installation (large dependency)

**Usage:**
```bash
# Same interface as evaluate_semantic_simple.py
python scripts/evaluate_semantic_retrievers.py --dataset simple
```

**Note:** Use `evaluate_semantic_simple.py` if you want to avoid PyTorch dependency. Results are comparable.

---

### 3. `generate_charts.py`

**Purpose:** Generate bar charts comparing Base vs Hybrid+Rerank retrievers.

**Features:**
- ✅ Creates 3 charts (simple, reasoning, improvement)
- ✅ Side-by-side bar comparisons
- ✅ Modern color palette
- ✅ High resolution (300 DPI)

**Usage:**
```bash
python scripts/generate_charts.py
```

**Data Source:**
- Hardcoded in script (update `SIMPLE_DATA` and `REASONING_DATA` dictionaries)

**Output Files:**
- `docs/images/semantic_eval_simple.png`
- `docs/images/semantic_eval_reasoning.png`
- `docs/images/semantic_eval_improvement.png`

**Customization:**
```python
# Edit these dictionaries in the script
SIMPLE_DATA = {
    'Base': {
        'Faithfulness': 0.171,
        'Relevancy': 0.231,
        # ...
    },
    'Hybrid+Rerank': {
        # ...
    }
}
```

---

### 4. `generate_trace_comparison.py`

**Purpose:** Generate visual comparison diagram of Base vs Hybrid+Rerank traces.

**Features:**
- ✅ Side-by-side trace visualization
- ✅ Shows latency, cost, metrics
- ✅ Alternative to LangSmith screenshots

**Usage:**
```bash
python scripts/generate_trace_comparison.py
```

**Output Files:**
- `docs/images/langsmith_trace_comparison.png`

**Customization:**
- Edit trace content arrays in `create_trace_comparison()` function

---

## Dependencies

### Required for All Scripts

```txt
python>=3.8
```

### For Semantic Evaluation

```bash
pip install scikit-learn>=1.3.0
pip install pandas>=2.0.0
pip install numpy>=1.24.0
pip install python-dotenv>=1.0.0
```

### For Chart Generation

```bash
pip install matplotlib>=3.5.0
```

### For RAG Pipeline (Backend)

```bash
pip install openai>=1.0.0
pip install qdrant-client>=1.8.0
pip install langchain>=0.1.0
pip install langchain-openai>=0.0.2
pip install cohere>=4.37  # For Hybrid+Rerank only
```

### Optional (LangSmith Tracking)

```bash
pip install langsmith>=0.0.70
```

### Complete Installation

```bash
# Install all dependencies at once
pip install -r requirements.txt
```

---

## Output Files

### Evaluation Reports

**Location:** `reports/`

**Files Created:**
- `semantic_evaluation_simple_YYYYMMDD_HHMMSS.json`
- `semantic_evaluation_reasoning_YYYYMMDD_HHMMSS.json`
- `semantic_comparison_simple_YYYYMMDD_HHMMSS.csv`
- `semantic_comparison_reasoning_YYYYMMDD_HHMMSS.csv`
- `semantic_evaluation_simple_YYYYMMDD_HHMMSS.md`
- `semantic_evaluation_reasoning_YYYYMMDD_HHMMSS.md`

**JSON Structure:**
```json
{
  "evaluation_date": "2025-10-19T22:34:56",
  "dataset": "simple",
  "method": "TF-IDF + Cosine Similarity",
  "base_retriever": [
    {
      "query": "What is compound interest?",
      "expected_answer": "...",
      "generated_answer": "...",
      "faithfulness": 0.107,
      "relevancy": 0.076,
      "precision": 0.004,
      "recall": 0.014
    }
  ],
  "hybrid_retriever": [...],
  "summary": [...]
}
```

### Visualization Files

**Location:** `docs/images/`

**Files Created:**
- `semantic_eval_simple.png` (159 KB)
- `semantic_eval_reasoning.png` (163 KB)
- `semantic_eval_improvement.png` (161 KB)
- `langsmith_trace_comparison.png`

**Specifications:**
- Format: PNG
- Resolution: 300 DPI
- Size: ~12" × 7" (comparison), ~10" × 7" (improvement)

---

## Troubleshooting

### Issue: ModuleNotFoundError

**Problem:**
```
ModuleNotFoundError: No module named 'sklearn'
```

**Solution:**
```bash
pip install scikit-learn pandas numpy
```

---

### Issue: Qdrant Connection Failed

**Problem:**
```
Error: Failed to connect to Qdrant at http://localhost:6333
```

**Solution:**
1. Start Qdrant:
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   # OR
   ./qdrant  # If using standalone binary
   ```

2. Verify connection:
   ```bash
   curl http://localhost:6333
   ```

3. Check `.env` file:
   ```bash
   QDRANT_URL=http://localhost:6333
   ```

---

### Issue: OPENAI_API_KEY Not Set

**Problem:**
```
Error: OPENAI_API_KEY not found in environment
```

**Solution:**
1. Create/edit `.env` file:
   ```bash
   OPENAI_API_KEY=sk-...
   ```

2. Verify:
   ```bash
   grep OPENAI_API_KEY .env
   ```

---

### Issue: Charts Missing Emojis

**Problem:**
```
UserWarning: Glyph 128269 (\N{LEFT-POINTING MAGNIFYING GLASS}) missing from font(s) DejaVu Sans.
```

**Solution:**
- This is a warning, not an error
- Charts are generated successfully
- Emojis appear as squares (cosmetic issue only)
- To fix: Install system fonts with emoji support

---

### Issue: LangSmith Logging Failed

**Problem:**
```
WARNING:__main__:LangSmith logging failed: 422 Client Error
```

**Solution:**
- This is expected (known validation error with `run_type`)
- Evaluation continues successfully
- Metrics are still computed and saved
- LangSmith logging is optional

**To disable warning:**
```bash
# In .env, comment out:
# LANGCHAIN_TRACING_V2=true
```

---

### Issue: Evaluation Takes Too Long

**Problem:**
Evaluation runs for >30 minutes.

**Solution:**
1. Check internet connection (API calls)
2. Verify Qdrant is running locally (not cloud)
3. Reduce dataset size for testing:
   ```python
   # Edit dataset file to include fewer queries
   head -5 evaluation/golden_set.jsonl > evaluation/test_set.jsonl
   ```

---

### Issue: Out of Memory

**Problem:**
```
MemoryError: Unable to allocate array
```

**Solution:**
1. Close other applications
2. Use `evaluate_semantic_simple.py` (lighter than PyTorch version)
3. Process datasets one at a time

---

## Best Practices

### 1. Run Evaluations in Order

```bash
# 1. Simple dataset first (faster, validates setup)
python scripts/evaluate_semantic_simple.py --dataset simple

# 2. Reasoning dataset (more comprehensive)
python scripts/evaluate_semantic_simple.py --dataset reasoning

# 3. Generate charts
python scripts/generate_charts.py
python scripts/generate_trace_comparison.py
```

### 2. Save Results with Timestamps

Scripts automatically add timestamps to output files. To keep results organized:

```bash
# Results are automatically saved as:
# reports/semantic_evaluation_simple_20251019_223456.json
# reports/semantic_evaluation_reasoning_20251019_223804.json

# Archive old results
mkdir -p reports/archive
mv reports/semantic_evaluation_simple_2025* reports/archive/
```

### 3. Version Control

```bash
# Commit scripts (always)
git add scripts/

# Commit reports (optional, for history)
git add reports/*.json reports/*.csv reports/*.md

# Don't commit large image files repeatedly
# Keep latest version only
git add docs/images/*.png
```

### 4. Reproducibility

To ensure reproducibility:

1. **Document environment:**
   ```bash
   pip freeze > requirements_frozen.txt
   ```

2. **Save datasets:**
   - Keep `evaluation/golden_set.jsonl` unchanged
   - Version control dataset files

3. **Document random seeds:**
   - TF-IDF vectorizer is deterministic
   - OpenAI API calls may have slight variations

4. **Archive evaluation results:**
   ```bash
   # Save complete evaluation state
   tar -czf evaluation_20251019.tar.gz \
     reports/ \
     docs/images/ \
     evaluation/
   ```

---

## Advanced Usage

### Custom Dataset

1. Create new JSONL file:
   ```bash
   cat > evaluation/custom_set.jsonl << EOF
   {"query": "Your question?", "expected_answer": "Expected answer"}
   {"query": "Another question?", "expected_answer": "Another answer"}
   EOF
   ```

2. Modify script to use custom dataset:
   ```python
   # In evaluate_semantic_simple.py, add new choice
   parser.add_argument("--dataset", choices=["simple", "reasoning", "custom"])
   
   # Add custom path
   elif args.dataset == "custom":
       dataset_path = "evaluation/custom_set.jsonl"
   ```

### Batch Evaluation

Run multiple evaluations:

```bash
#!/bin/bash
# batch_evaluate.sh

for dataset in simple reasoning; do
  echo "Evaluating $dataset dataset..."
  python scripts/evaluate_semantic_simple.py --dataset $dataset
  
  if [ $? -eq 0 ]; then
    echo "✓ $dataset evaluation complete"
  else
    echo "✗ $dataset evaluation failed"
  fi
done

# Generate charts after all evaluations
python scripts/generate_charts.py
```

### Update Charts with Latest Data

```bash
# 1. Find latest evaluation results
latest_simple=$(ls -t reports/semantic_evaluation_simple_*.json | head -1)
latest_reasoning=$(ls -t reports/semantic_evaluation_reasoning_*.json | head -1)

# 2. Extract metrics and update generate_charts.py
python << EOF
import json

with open('$latest_simple') as f:
    simple_data = json.load(f)
    
# Extract summary metrics
base_faith = simple_data['summary'][0]['Faithfulness']
hybrid_faith = simple_data['summary'][1]['Faithfulness']

print(f"Update SIMPLE_DATA in generate_charts.py:")
print(f"  Base Faithfulness: {base_faith}")
print(f"  Hybrid Faithfulness: {hybrid_faith}")
EOF

# 3. Re-generate charts
python scripts/generate_charts.py
```

---

## Maintenance

### Updating Scripts

When modifying scripts, ensure:

1. **Paths remain relative:**
   ```python
   # Good
   dataset_path = "evaluation/golden_set.jsonl"
   
   # Bad
   dataset_path = "/Users/username/project/evaluation/golden_set.jsonl"
   ```

2. **Timestamps are unique:**
   ```python
   timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
   ```

3. **Error handling is robust:**
   ```python
   try:
       results = evaluate(...)
   except Exception as e:
       logger.error(f"Evaluation failed: {e}")
       sys.exit(1)
   ```

4. **Dependencies are documented:**
   - Update `requirements.txt`
   - Update this README

### Testing Scripts

Before committing changes:

```bash
# 1. Lint
python -m pylint scripts/*.py

# 2. Test on sample data
head -3 evaluation/golden_set.jsonl > evaluation/test.jsonl
python scripts/evaluate_semantic_simple.py --dataset test

# 3. Verify outputs
ls -lh reports/semantic_evaluation_*
ls -lh docs/images/*.png
```

---

## Support

For issues or questions:

1. Check [Troubleshooting](#troubleshooting) section
2. Review script docstrings: `python scripts/script_name.py --help`
3. Check evaluation documentation: `docs/Evaluation_RAGAS_Semantic.md`
4. Review LangSmith guide: `docs/LANGSMITH_SCREENSHOT_CAPTURE_GUIDE.md`

---

**Last Updated:** October 20, 2025  
**Version:** 1.0  
**Status:** ✅ Production-ready

