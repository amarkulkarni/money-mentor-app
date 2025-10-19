# Advanced Retriever Implementation

## Overview

MoneyMentor now supports two retrieval modes for enhanced RAG pipeline performance:

1. **Base Retriever** - Traditional similarity search
2. **Advanced Retriever** - MultiQuery expansion for improved context quality

Both modes are fully integrated with LangSmith for tracking and comparison.

---

## Retrieval Modes

### 🔍 Base Retriever

**Mode:** `base`

**How it works:**
- Generates a single embedding for the user query
- Performs similarity search in Qdrant
- Retrieves k most similar chunks
- Fast and cost-effective

**Use cases:**
- Straightforward queries
- Well-defined questions
- Cost-sensitive applications

**Example:**
```python
result = get_finance_answer("What is compound interest?", mode="base", k=3)
```

**Output:**
- Retrieved: 3 documents
- API calls: 1 embedding call + 1 search

---

### 🚀 Advanced Retriever (MultiQuery)

**Mode:** `advanced`

**How it works:**
- Uses LLM to generate multiple query variations
- Each variation represents a different perspective
- Performs parallel searches for all variations
- De-duplicates and ranks results
- Retrieves more diverse, comprehensive context

**Use cases:**
- Complex or ambiguous queries
- Questions requiring multiple perspectives
- Queries where context quality is critical

**Example:**
```python
result = get_finance_answer("What is compound interest?", mode="advanced", k=3)
```

**Output:**
- Retrieved: 6+ documents (from 3 query variations)
- API calls: 1 LLM call + 3 embedding calls + 3 searches
- Generated queries:
  - "What does compound interest mean and how is it calculated?"
  - "Can you explain the concept of compound interest and its implications for savings?"
  - "How does compound interest differ from simple interest?"

---

## Technical Implementation

### Architecture

```
Query → get_retriever(mode) → Retriever → Documents → LLM → Answer
                ↓
        base or advanced
                ↓
        ┌──────────────────────┐
        │  Base: Similarity    │
        │  Advanced: MultiQuery│
        └──────────────────────┘
```

### Key Functions

#### `get_base_retriever()`
```python
def get_base_retriever(collection_name: str, k: int):
    vectorstore = Qdrant(
        client=get_qdrant_client(),
        collection_name=collection_name,
        embeddings=OpenAIEmbeddings(),
        content_payload_key="text"
    )
    return vectorstore.as_retriever(search_kwargs={"k": k})
```

#### `get_advanced_retriever()`
```python
def get_advanced_retriever(collection_name: str, k: int):
    vectorstore = Qdrant(...)
    base_retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    
    advanced_retriever = MultiQueryRetriever.from_llm(
        retriever=base_retriever,
        llm=ChatOpenAI(model="gpt-4o-mini")
    )
    return advanced_retriever
```

#### `get_finance_answer()` - Updated Signature
```python
def get_finance_answer(
    query: str,
    k: int = 5,
    collection_name: str = COLLECTION_NAME,
    mode: str = "base",  # ← New parameter
    return_context: bool = False
) -> Dict[str, Any]:
```

---

## LangSmith Integration

### Tracking Features

Every retrieval run is logged to LangSmith with:

**Inputs:**
- Query text
- Retrieval mode (base/advanced)
- Number of chunks requested (k)
- Collection name

**Outputs:**
- Generated answer
- Number of documents retrieved
- Number of unique sources

**Metadata:**
- Retriever mode
- Model used (GPT-4o-mini)
- Embedding model (text-embedding-3-small)
- Retrieved contexts (first 500 chars)
- Source files and scores

**Tags:**
- `moneymentor`
- `rag`
- `base_retriever` or `advanced_retriever`

### Viewing in LangSmith

1. Go to: https://smith.langchain.com/o/default/projects/p/MoneyMentor
2. Filter by tags: `base_retriever` or `advanced_retriever`
3. Compare runs side-by-side
4. Analyze:
   - Context quality
   - Answer accuracy
   - Latency
   - Token usage
   - Cost per query

---

## Usage Examples

### API Endpoint

```python
# app/main.py
@app.post("/api/chat")
def chat(request: ChatRequest):
    # Use base mode by default
    result = get_finance_answer(
        query=request.question,
        mode="base",  # or "advanced"
        k=5
    )
    return ChatResponse(**result)
```

### Direct Python

```python
from app.rag_pipeline import get_finance_answer

# Base retrieval
result_base = get_finance_answer(
    "What is compound interest?",
    mode="base",
    k=3
)

# Advanced retrieval
result_advanced = get_finance_answer(
    "What is compound interest?",
    mode="advanced",
    k=3
)

print(f"Base sources: {len(result_base['sources'])}")
print(f"Advanced sources: {len(result_advanced['sources'])}")
```

### Evaluation Script

```python
# Modify app/evaluation/evaluator.py to test both modes
for mode in ["base", "advanced"]:
    result = get_finance_answer(
        query=test_query,
        mode=mode,
        k=5,
        return_context=True
    )
    # Compute RAGAS metrics
    # Compare results
```

---

## Performance Comparison

| Metric | Base Retriever | Advanced Retriever |
|--------|----------------|-------------------|
| API Calls | 1 embedding + 1 search | 1 LLM + 3 embeddings + 3 searches |
| Documents Retrieved | k (e.g., 3) | ~2-3× k (e.g., 6-9) |
| Latency | ~0.5s | ~2-3s |
| Cost per Query | $0.0001 | $0.0005 |
| Context Diversity | Lower | Higher |
| Best For | Simple queries | Complex/ambiguous queries |

---

## Configuration

### Environment Variables

No additional environment variables required. Uses existing:
- `OPENAI_API_KEY` - For embeddings and LLM
- `LANGCHAIN_API_KEY` - For LangSmith tracking
- `LANGCHAIN_TRACING_V2=true`
- `LANGCHAIN_PROJECT=MoneyMentor`

### Dependencies

Updated `requirements.txt`:
```
langchain>=0.1.0
langchain-community>=0.0.20
langchain-openai>=0.0.5
```

No additional packages needed - MultiQueryRetriever is part of LangChain core.

---

## Deprecation Warnings

You may see warnings:
```
LangChainDeprecationWarning: The class `Qdrant` was deprecated...
```

**Action:** These are warnings only. The code works correctly. For future-proofing, we can migrate to `langchain-qdrant` package when needed.

---

## Testing

### Quick Test

```bash
cd /Users/amar.kulkarni/code/money-mentor-app/moneymentor

python3 << 'EOF'
import sys
sys.path.insert(0, 'app')
from rag_pipeline import get_finance_answer

# Test both modes
for mode in ["base", "advanced"]:
    result = get_finance_answer("What is compound interest?", mode=mode, k=3)
    print(f"{mode.upper()}: {len(result['sources'])} sources")
EOF
```

### Expected Output

```
BASE: 3 sources
ADVANCED: 6 sources
```

---

## Future Enhancements

1. **Contextual Compression Retriever**
   - Add LLM-based compression to filter irrelevant chunks
   - Reduce context size while maintaining quality

2. **Hybrid Search**
   - Combine keyword search (BM25) with vector search
   - Better for queries with specific terms

3. **Reranking**
   - Add cross-encoder reranking after retrieval
   - Improve relevance ordering

4. **Adaptive Mode Selection**
   - Automatically choose mode based on query complexity
   - Balance cost and quality

5. **Custom Query Templates**
   - Fine-tune MultiQuery prompt for financial domain
   - Generate more relevant query variations

---

## Troubleshooting

### Issue: "page_content validation error"

**Solution:** Ensure Qdrant vectorstore uses `content_payload_key="text"`:
```python
vectorstore = Qdrant(
    ...,
    content_payload_key="text"
)
```

### Issue: MultiQuery generates irrelevant variations

**Solution:** Customize the query generation prompt in MultiQueryRetriever:
```python
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["question"],
    template="Generate 3 variations of this financial question: {question}"
)
```

### Issue: High latency with advanced mode

**Solution:** Reduce k or use base mode for non-critical queries.

---

## Summary

✅ **Implemented:**
- Base and Advanced retrieval modes
- LangSmith tracking for both modes
- Flexible API with mode selection
- Comprehensive documentation

✅ **Benefits:**
- Improved context quality with MultiQuery
- Side-by-side comparison in LangSmith
- Flexibility to choose based on query type
- Full observability

✅ **Next Steps:**
- Run evaluation on both modes
- Compare RAGAS metrics
- Optimize mode selection strategy
- Consider additional retrieval strategies

---

**Last Updated:** October 19, 2025  
**Version:** 1.0

