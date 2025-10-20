# Quick Reference: Evaluation Scripts

**Last Updated:** October 20, 2025

---

## 🚀 Quick Start (3 Commands)

```bash
# 1. Activate environment
source venv/bin/activate

# 2. Run evaluation (10 min)
python scripts/evaluate_semantic_simple.py --dataset reasoning

# 3. Generate charts (5 sec)
python scripts/generate_charts.py
```

---

## 📊 All Scripts

| Command | What It Does | Time |
|---------|--------------|------|
| `python scripts/evaluate_semantic_simple.py --dataset simple` | Evaluate 15 simple queries | ~5 min |
| `python scripts/evaluate_semantic_simple.py --dataset reasoning` | Evaluate 12 reasoning queries | ~5 min |
| `python scripts/generate_charts.py` | Create 3 bar charts | ~5 sec |
| `python scripts/generate_trace_comparison.py` | Create trace diagram | ~3 sec |

---

## 📁 Input Files

| File | Queries | Type |
|------|---------|------|
| `evaluation/golden_set.jsonl` | 15 | Simple lookups |
| `evaluation/golden_set_reasoning.jsonl` | 12 | Complex reasoning |

---

## 📄 Output Files

### Reports (in `reports/`)
- `semantic_evaluation_{dataset}_{timestamp}.json` - Detailed results
- `semantic_comparison_{dataset}_{timestamp}.csv` - Summary table
- `semantic_evaluation_{dataset}_{timestamp}.md` - Markdown report

### Charts (in `docs/images/`)
- `semantic_eval_simple.png` - Simple dataset chart
- `semantic_eval_reasoning.png` - Reasoning dataset chart
- `semantic_eval_improvement.png` - Improvement analysis
- `langsmith_trace_comparison.png` - Trace diagram

---

## 🔧 Common Tasks

### Run Complete Evaluation

```bash
# Run both datasets
python scripts/evaluate_semantic_simple.py --dataset simple
python scripts/evaluate_semantic_simple.py --dataset reasoning

# Generate all visuals
python scripts/generate_charts.py
python scripts/generate_trace_comparison.py

# View results
ls -lh reports/semantic_evaluation_*
```

### Update Charts

```bash
# 1. Edit data in generate_charts.py (lines 20-50)
# 2. Regenerate
python scripts/generate_charts.py
```

### Test Setup

```bash
# Quick test (1 query)
head -1 evaluation/golden_set.jsonl > evaluation/test.jsonl
# Edit evaluate_semantic_simple.py to use test.jsonl
python scripts/evaluate_semantic_simple.py
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| Can't connect to Qdrant | Start Qdrant: `docker run -p 6333:6333 qdrant/qdrant` |
| `OPENAI_API_KEY` missing | Check `.env` file exists with API key |
| Slow evaluation | Check internet connection, verify Qdrant is local |

---

## 📚 Full Documentation

See `scripts/README.md` for complete documentation.

---

**Quick Help:**
```bash
python scripts/evaluate_semantic_simple.py --help
```

