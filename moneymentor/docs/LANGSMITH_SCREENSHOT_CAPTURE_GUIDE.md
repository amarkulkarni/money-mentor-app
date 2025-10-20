# LangSmith Screenshot Capture Guide

**Purpose:** Capture evaluation traces showing Base vs Hybrid+Rerank retrievers for documentation.

---

## 🎯 What to Capture

You need **2 screenshots** showing:
1. Base retriever evaluation trace
2. Hybrid+Rerank retriever evaluation trace

Each screenshot should show:
- ✅ Query input
- ✅ Retrieved document chunks (contexts)
- ✅ Generated answer
- ✅ Semantic scoring metrics (if logged)
- ✅ Execution time
- ✅ Token usage

---

## 📋 Step-by-Step Instructions

### Step 1: Access LangSmith Dashboard

1. Go to: https://smith.langchain.com/
2. Log in with your account
3. Select your project: **"MoneyMentor"**

### Step 2: Find Base Retriever Runs

**Option A: From Recent Evaluation**
1. Click on "Traces" in the left sidebar
2. Filter by tags:
   - Tag: `moneymentor`
   - Tag: `semantic_evaluation_tfidf`
   - Tag: `retriever=base`
3. Look for runs named: `"Semantic_Eval_base_simple"` or `"Semantic_Eval_base_reasoning"`

**Option B: Search by Date**
1. Filter runs from: **October 19, 2025 (today)**
2. Look for runs around: **22:30-23:00**
3. Find runs with "base" in the name

### Step 3: Select a Good Example Run

**Choose a run that shows:**
- ✅ A complex query (preferably from reasoning dataset)
- ✅ Clear retrieved contexts (5 chunks visible)
- ✅ Complete generated answer
- ✅ All metadata visible

**Good example queries:**
- "Compare traditional IRA vs Roth IRA..."
- "How do compound interest and inflation interact..."
- "Explain how diversification reduces portfolio risk..."

### Step 4: Capture Base Retriever Screenshot

1. Click on the selected run to open details
2. Expand all relevant sections:
   - **Inputs:** Should show the query
   - **Outputs:** Should show the answer and metrics
   - **Metadata:** Should show retrieval mode, contexts
3. Scroll to fit as much information as possible
4. Take screenshot (Cmd+Shift+4 on Mac, Win+Shift+S on Windows)
5. Save as: `docs/images/langsmith_trace_base.png`

**What should be visible:**
```
┌─────────────────────────────────────────┐
│ Run: Semantic_Eval_base_reasoning       │
│ Status: ✓ Success                       │
│ Duration: ~1.2s                         │
│                                         │
│ 📥 INPUTS                               │
│ query: "Compare traditional IRA vs..."  │
│ mode: "base"                            │
│ dataset: "reasoning"                    │
│                                         │
│ 📤 OUTPUTS                              │
│ generated_answer: "Traditional IRAs..." │
│ num_contexts: 5                         │
│ faithfulness: 0.156                     │
│ relevancy: 0.241                        │
│ precision: 0.023                        │
│ recall: 0.048                           │
│                                         │
│ 🔍 RETRIEVED CONTEXTS (sample)          │
│ 1. "A traditional IRA allows..."        │
│ 2. "Roth IRA contributions are..."      │
│ ...                                     │
└─────────────────────────────────────────┘
```

### Step 5: Find Hybrid+Rerank Retriever Runs

1. Go back to "Traces"
2. Filter by tags:
   - Tag: `moneymentor`
   - Tag: `semantic_evaluation_tfidf`
   - Tag: `retriever=hybrid_rerank`
3. Look for runs named: `"Semantic_Eval_advanced_reasoning"`

**Tip:** Try to find a run with the **same query** as your Base screenshot for easy comparison!

### Step 6: Capture Hybrid+Rerank Screenshot

1. Click on the selected run
2. Expand all sections (Inputs, Outputs, Metadata)
3. Take screenshot
4. Save as: `docs/images/langsmith_trace_hybrid.png`

**What should be visible:**
```
┌─────────────────────────────────────────┐
│ Run: Semantic_Eval_advanced_reasoning   │
│ Status: ✓ Success                       │
│ Duration: ~1.8s                         │
│                                         │
│ 📥 INPUTS                               │
│ query: "Compare traditional IRA vs..."  │
│ mode: "advanced"                        │
│ dataset: "reasoning"                    │
│                                         │
│ 📤 OUTPUTS                              │
│ generated_answer: "Traditional IRAs..." │
│ num_contexts: 5                         │
│ faithfulness: 0.162 (↑ vs base)         │
│ relevancy: 0.248 (↑ vs base)            │
│ precision: 0.023                        │
│ recall: 0.048                           │
│                                         │
│ 🔍 RETRIEVED CONTEXTS (sample)          │
│ 1. "Traditional IRA tax treatment..."   │
│ 2. "Roth IRA advantages include..."     │
│ ...                                     │
│                                         │
│ 🚀 HYBRID RETRIEVAL DETAILS             │
│ BM25 matches: 20                        │
│ Vector matches: 20                      │
│ Ensemble results: 24                    │
│ Reranked to: 5                          │
└─────────────────────────────────────────┘
```

---

## 📸 Screenshot Best Practices

### Do's ✅
- ✅ Use high resolution (at least 1920x1080)
- ✅ Expand all relevant sections
- ✅ Show complete query and answer
- ✅ Include all metrics
- ✅ Capture in light mode (better readability)
- ✅ Crop to remove unnecessary UI elements

### Don'ts ❌
- ❌ Don't capture partial information
- ❌ Don't use low resolution
- ❌ Don't include sensitive API keys
- ❌ Don't show unrelated runs or projects

---

## 🔍 Alternative: What If Runs Don't Show Metrics?

**Problem:** The semantic evaluation script had LangSmith logging issues (run_type validation error).

**Solution 1: Use evaluation JSON files**
```bash
# View detailed results
cat reports/semantic_evaluation_reasoning_*.json | jq '.base_retriever[] | select(.query | contains("IRA"))'
```

**Solution 2: Create comparison table manually**
Use the data from `reports/semantic_evaluation_*.json` to create a comparison table in markdown.

**Solution 3: Run evaluation again with fixed LangSmith logging**
1. Fix the `run_type` in `scripts/evaluate_semantic_simple.py`
2. Change `run_type="evaluation"` to `run_type="chain"`
3. Re-run evaluation: `python scripts/evaluate_semantic_simple.py --dataset reasoning`

---

## 🎨 Alternative: Create Comparison Diagram

If screenshots are difficult, create a side-by-side comparison diagram showing:

```
┌─────────────────┬─────────────────┐
│   BASE          │  HYBRID+RERANK  │
├─────────────────┼─────────────────┤
│ Mode: base      │ Mode: advanced  │
│ Latency: 0.8s   │ Latency: 1.8s   │
│ Cost: $0.00002  │ Cost: $0.00025  │
│                 │                 │
│ Faithfulness:   │ Faithfulness:   │
│   0.145         │   0.156 (+1.1%) │
│                 │                 │
│ Relevancy:      │ Relevancy:      │
│   0.230         │   0.241 (+1.1%) │
└─────────────────┴─────────────────┘
```

---

## 📋 Checklist

Before moving forward, ensure you have:

- [ ] Accessed LangSmith dashboard
- [ ] Found Base retriever runs
- [ ] Found Hybrid+Rerank retriever runs
- [ ] Captured Base screenshot (langsmith_trace_base.png)
- [ ] Captured Hybrid+Rerank screenshot (langsmith_trace_hybrid.png)
- [ ] Both screenshots show the same query (for comparison)
- [ ] Screenshots are high quality and readable
- [ ] Screenshots saved in `docs/images/`

---

## 🚀 Next Steps After Capturing

Once you have the screenshots:

1. Verify they're saved in the correct location:
   ```bash
   ls -lh docs/images/langsmith_trace_*.png
   ```

2. Update documentation to embed them:
   ```markdown
   **Base Retriever Trace:**
   ![Base Retriever LangSmith Trace](images/langsmith_trace_base.png)
   
   **Hybrid+Rerank Retriever Trace:**
   ![Hybrid+Rerank LangSmith Trace](images/langsmith_trace_hybrid.png)
   ```

3. Commit the images:
   ```bash
   git add docs/images/langsmith_trace_*.png
   git commit -m "docs: Add LangSmith evaluation trace screenshots"
   ```

---

## 💡 Tips

- **Best query to use:** "Compare traditional IRA vs Roth IRA..." (shows multi-source synthesis)
- **Best time to capture:** Right after running evaluation (traces are fresh)
- **Best view:** Expand all sections but keep it concise (single scrollable view)
- **Format:** PNG for best compatibility with markdown

---

## ❓ Troubleshooting

**Issue:** Can't find runs in LangSmith
- **Solution:** Check if `LANGCHAIN_TRACING_V2=true` in your `.env`
- **Solution:** Verify `LANGCHAIN_API_KEY` is set correctly
- **Solution:** Re-run evaluation to generate fresh traces

**Issue:** Runs show error status
- **Solution:** Check the error message in LangSmith
- **Solution:** The validation error is known (run_type issue)
- **Solution:** Use the JSON reports as alternative

**Issue:** Screenshots too large
- **Solution:** Crop unnecessary parts
- **Solution:** Compress using: `convert input.png -quality 85 output.png`

---

**Document Version:** 1.0  
**Last Updated:** October 19, 2025  
**Status:** Ready for screenshot capture

