# LangSmith Tagging & Screenshot Guide

**Purpose:** Document how to tag evaluation runs in LangSmith and capture comparison screenshots for the evaluation report.

---

## 1. Tagging Runs in LangSmith

### Access Your Runs

1. Navigate to: https://smith.langchain.com/
2. Go to **Projects** → **MoneyMentor**
3. Filter by runs containing "Evaluation" in the name

### Apply Tags to Each Run

#### For Base Retriever Run

**Run Name:** `MoneyMentor RAG Evaluation (base)`  
**Date:** 2025-10-19 14:33:XX

**Steps:**
1. Click on the run
2. Click **"Edit"** or **"Add Tags"** button (top right)
3. Add these tags (comma-separated):
   ```
   retriever=base, mode=base, production_candidate
   ```
4. Click **"Save"**

#### For MultiQuery Run

**Run Name:** `MoneyMentor RAG Evaluation (advanced)` (earlier timestamp)  
**Date:** 2025-10-19 14:34:34

**Steps:**
1. Click on the run
2. Click **"Edit"** or **"Add Tags"**
3. Add these tags:
   ```
   retriever=multiquery, mode=advanced, deprecated, no_improvement
   ```
4. Click **"Save"**

#### For MultiQuery + Compression Run

**Run Name:** `MoneyMentor RAG Evaluation (advanced)` (latest timestamp)  
**Date:** 2025-10-19 15:21:12

**Steps:**
1. Click on the run
2. Click **"Edit"** or **"Add Tags"**
3. Add these tags:
   ```
   retriever=multiquery_compression, mode=advanced, failed_experiment, has_failures
   ```
4. Click **"Save"**

### Verify Tags

After tagging, test the filters:
- Filter by `retriever=base` → Should show 1 run
- Filter by `mode=advanced` → Should show 2 runs
- Filter by `deprecated` → Should show MultiQuery run only

---

## 2. Required Screenshots

### Screenshot 1: Run Comparison Dashboard

**Location:** LangSmith → MoneyMentor project → Runs list

**What to capture:**
- All 3 evaluation runs visible in a table
- Columns showing:
  - Run Name
  - Status (Completed)
  - Duration (seconds)
  - Total Cost (dollars)
  - Success Rate (%)
  - Timestamp

**Steps:**
1. Go to project page
2. Filter to show only "Evaluation" runs (search bar)
3. Sort by timestamp (newest first)
4. Adjust columns to show: Name, Status, Duration, Cost, Success Rate
5. Take screenshot (Cmd+Shift+4 on Mac, Win+Shift+S on Windows)
6. Save as: `screenshots/langsmith_run_comparison.png`

**Expected view:**
```
Run Name                                    Status      Duration    Cost        Success
─────────────────────────────────────────────────────────────────────────────────────
MoneyMentor RAG Evaluation (advanced)       Completed   180s        $0.018      87%
MoneyMentor RAG Evaluation (advanced)       Completed   45s         $0.0045     100%
MoneyMentor RAG Evaluation (base)           Completed   10s         $0.0003     100%
```

### Screenshot 2: Cost Breakdown Chart

**Location:** LangSmith → Select run → **"Analytics"** or **"Costs"** tab

**What to capture:**
- Bar chart or line graph comparing costs across runs
- X-axis: Run name/mode
- Y-axis: Total cost in dollars
- Clear visual showing 15× and 60× increases

**Steps:**
1. Click on one of the evaluation runs
2. Navigate to **"Analytics"** tab
3. Find or create a cost comparison view
4. If no built-in chart, take screenshots of each run's cost individually:
   - Base run: $0.0003 total
   - MultiQuery run: $0.0045 total
   - Compression run: $0.018 total
5. Save as: `screenshots/langsmith_cost_comparison.png`

**Alternative (if no chart available):**
Create a simple comparison table screenshot showing costs side-by-side.

### Screenshot 3: Latency Distribution

**Location:** LangSmith → Analytics → Latency metrics

**What to capture:**
- Distribution of query latencies for each retriever mode
- Box plot or histogram showing:
  - Median latency
  - P95 latency
  - Min/Max latency
- Clear visual showing 3× and 10× increases

**Steps:**
1. Go to Analytics dashboard
2. Select "Latency" metric
3. Group by run or tag (retriever type)
4. Capture the distribution chart
5. Save as: `screenshots/langsmith_latency_distribution.png`

**Expected metrics:**
```
Base: Median 0.8s, P95 1.2s
MultiQuery: Median 2.5s, P95 3.5s  
Compression: Median 10s, P95 14s
```

### Screenshot 4: Metadata View with RAGAS Metrics

**Location:** LangSmith → Select run → **"Metadata"** or **"Inputs/Outputs"** tab

**What to capture:**
- JSON view of run metadata showing RAGAS scores
- Should include:
  - evaluation_type: "RAGAS"
  - retrieval_mode: "base" / "advanced"
  - faithfulness: 0.0
  - answer_relevancy: 1.0
  - context_precision: 0.0
  - context_recall: 0.0

**Steps:**
1. Click on Base retriever run
2. Navigate to **"Metadata"** tab
3. Find the RAGAS metrics section
4. Take screenshot showing the JSON
5. Save as: `screenshots/langsmith_ragas_base.png`
6. Repeat for MultiQuery run → `screenshots/langsmith_ragas_multiquery.png`
7. Repeat for Compression run → `screenshots/langsmith_ragas_compression.png`

**Expected JSON:**
```json
{
  "evaluation_type": "RAGAS",
  "retrieval_mode": "base",
  "num_contexts": 5,
  "faithfulness": 0.0,
  "answer_relevancy": 1.0,
  "context_precision": 0.0,
  "context_recall": 0.0
}
```

### Screenshot 5: Failed Query Detail (Compression Run)

**Location:** LangSmith → Compression run → Failed queries

**What to capture:**
- Details of query #2 ("What is the 50/30/20 budgeting rule?")
- Show the error message: "No relevant context found"
- Show empty retrieved documents or filtered-out context

**Steps:**
1. Open the Compression evaluation run
2. Find query #2 or #13 (the failed ones)
3. Click to view details
4. Capture the trace showing:
   - Query input
   - Retrieved documents (if any)
   - Compression step (filtered everything)
   - Final error/empty context
5. Save as: `screenshots/langsmith_failed_query.png`

**Purpose:** Visual evidence of over-aggressive filtering problem.

---

## 3. Screenshot Storage & Usage

### Directory Structure

Create this structure:
```
moneymentor/
├── docs/
│   ├── Evaluation_RAGAS_Updated.md
│   └── screenshots/
│       ├── langsmith_run_comparison.png
│       ├── langsmith_cost_comparison.png
│       ├── langsmith_latency_distribution.png
│       ├── langsmith_ragas_base.png
│       ├── langsmith_ragas_multiquery.png
│       ├── langsmith_ragas_compression.png
│       └── langsmith_failed_query.png
```

### Create Directory

```bash
cd moneymentor/docs
mkdir -p screenshots
```

### Update Documentation

Once screenshots are captured, update `Evaluation_RAGAS_Updated.md`:

Replace placeholder sections with actual image references:

```markdown
### Screenshot 1: Run Comparison

![LangSmith Run Comparison](screenshots/langsmith_run_comparison.png)

*Figure 1: Comparison of three retrieval approaches in LangSmith. Note the 60× cost increase for compression with no quality improvement.*
```

Repeat for all screenshots.

---

## 4. Optional: Programmatic Tagging (Advanced)

If you want to tag runs programmatically via LangSmith API:

### Install LangSmith SDK

```bash
pip install langsmith
```

### Tag Script

Create `scripts/tag_langsmith_runs.py`:

```python
from langsmith import Client
import os

# Initialize client
client = Client(api_key=os.getenv("LANGCHAIN_API_KEY"))

# Define run IDs and their tags
# (Get run IDs from LangSmith UI → run → URL)
runs_to_tag = {
    "run_id_base_here": ["retriever=base", "mode=base", "production_candidate"],
    "run_id_multiquery_here": ["retriever=multiquery", "mode=advanced", "deprecated"],
    "run_id_compression_here": ["retriever=multiquery_compression", "mode=advanced", "failed_experiment"],
}

# Apply tags
for run_id, tags in runs_to_tag.items():
    try:
        client.update_run(
            run_id=run_id,
            tags=tags
        )
        print(f"✅ Tagged run {run_id[:8]}... with: {', '.join(tags)}")
    except Exception as e:
        print(f"❌ Failed to tag run {run_id[:8]}...: {e}")

print("\n✅ All runs tagged!")
```

### Run Tagging Script

```bash
python scripts/tag_langsmith_runs.py
```

---

## 5. Checklist

Before considering this task complete:

### Tagging
- [ ] Tagged Base retriever run with `retriever=base`
- [ ] Tagged MultiQuery run with `retriever=multiquery, deprecated`
- [ ] Tagged Compression run with `retriever=multiquery_compression, failed_experiment`
- [ ] Verified tags by filtering in LangSmith UI

### Screenshots
- [ ] Captured run comparison table
- [ ] Captured cost comparison (or individual costs)
- [ ] Captured latency distribution (or individual latencies)
- [ ] Captured RAGAS metadata for Base run
- [ ] Captured RAGAS metadata for MultiQuery run
- [ ] Captured RAGAS metadata for Compression run
- [ ] Captured failed query detail from Compression run
- [ ] Created `docs/screenshots/` directory
- [ ] Saved all screenshots with correct filenames

### Documentation
- [ ] Updated `Evaluation_RAGAS_Updated.md` with actual image paths
- [ ] Verified images render correctly in Markdown preview
- [ ] Committed all screenshots to git

### Git
- [ ] All documentation files committed
- [ ] All screenshots committed
- [ ] Descriptive commit message

---

## 6. Example Commit

Once everything is ready:

```bash
cd moneymentor

# Stage all new files
git add docs/Evaluation_RAGAS_Updated.md
git add docs/LANGSMITH_SCREENSHOT_GUIDE.md
git add docs/screenshots/*.png

# Commit
git commit -m "docs: Add comprehensive RAGAS evaluation report with LangSmith screenshots

- Created Evaluation_RAGAS_Updated.md with full analysis
- Compared Base vs MultiQuery vs MultiQuery+Compression retrievers
- Documented cost-benefit analysis (60× cost, 0× improvement)
- Added screenshot guide for LangSmith tagging and capture
- Included improvement plan: Hybrid Search + Reranking
- Tagged all evaluation runs in LangSmith

Completes rubric sections:
- Assessing Performance ✓
- Advanced Retrieval ✓  
- Improvement Plan ✓"

# Show commit
git log -1 --stat
```

---

**Last Updated:** October 19, 2025  
**Status:** Ready for screenshot capture  
**Estimated Time:** 15-20 minutes to tag and capture all screenshots

