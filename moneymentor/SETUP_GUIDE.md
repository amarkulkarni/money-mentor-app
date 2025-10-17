# MoneyMentor - Complete Setup Guide

This guide will walk you through setting up and running the complete MoneyMentor RAG pipeline.

## Prerequisites

- Python 3.9+
- Docker (for Qdrant)
- OpenAI API key

## Step 1: Install Dependencies

```bash
cd moneymentor
pip install -r requirements.txt
```

## Step 2: Set Up Environment Variables

Create a `.env` file in the moneymentor directory:

```bash
# .env
OPENAI_API_KEY=sk-your-openai-api-key-here
QDRANT_URL=http://localhost:6333
```

Or export them:

```bash
export OPENAI_API_KEY="sk-your-openai-api-key-here"
export QDRANT_URL="http://localhost:6333"
```

## Step 3: Start Qdrant Vector Database

```bash
docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant
```

Verify Qdrant is running:
```bash
curl http://localhost:6333
```

## Step 4: Add Your Documents

Place PDF or TXT files in the `data/` directory:

```bash
cd moneymentor
cp /path/to/your/financial-guide.pdf data/
cp /path/to/your/investing-101.pdf data/
```

## Step 5: Extract Text from Documents

```bash
cd app
python data_loader.py
```

This will:
- Scan `data/` for PDF and TXT files
- Extract text using PyMuPDF
- Save processed text to `app/data/processed/`

Expected output:
```
============================================================
MoneyMentor - Data Extraction Tool
============================================================

📂 Found 2 file(s) to process:
   - 2 PDF file(s)
   - 0 TXT file(s)

Processing: financial-guide.pdf
✅ Extracted 45 pages from financial-guide.pdf
💾 Saved processed text to data/processed/financial-guide.txt

✨ Processing complete! 2/2 files processed successfully.
```

## Step 6: Build Embeddings and Index

```bash
python rag_pipeline.py
```

This will:
1. Read processed text files
2. Chunk text (800 chars, 100 overlap)
3. Generate embeddings using OpenAI text-embedding-3-small
4. Index vectors in Qdrant collection "moneymentor_knowledge"

Expected output:
```
============================================================
Loading Knowledge Base into Vector Store
============================================================
📦 Ensuring collection 'moneymentor_knowledge' exists...
📂 Found 2 text file(s) to process
✂️  Text splitter: chunk_size=800, overlap=100
🔌 Initializing OpenAI embeddings (text-embedding-3-small)...

📄 Processing: financial-guide.txt
   ✂️  Split into 156 chunk(s)

✅ Created 312 total chunk(s) from 2 file(s)

🧮 Generating embeddings for 312 chunk(s)...
   (This may take a moment...)
   Processing batch 1/16
   Processing batch 2/16
   ...

✅ Generated 312 embedding vector(s)

💾 Upserting 312 vector(s) to Qdrant...
✅ Successfully upserted 312 point(s)

============================================================
✨ Knowledge Base Loading Complete!
============================================================
📊 Documents processed: 2
📊 Chunks created: 312
📊 Vectors indexed: 312
📊 Collection: moneymentor_knowledge
============================================================
```

## Step 7: Test a Query (CLI)

```bash
python rag_pipeline.py --query "How should I start investing?"
```

Expected output:
```
Testing query: 'How should I start investing?'
------------------------------------------------------------

📝 Answer:
Starting to invest is an excellent decision! Here are the key steps...
[GPT-4 generated answer based on your documents]

📚 Sources (5 found):
   1. financial-guide.txt (score: 0.876)
      When starting to invest, it's important to first understand...
   2. investing-101.txt (score: 0.845)
      The basics of investing begin with setting clear financial...

🤖 Model: gpt-4
```

## Step 8: Start the API Server

```bash
python main.py
```

The server will start at http://localhost:8000

Visit the interactive docs: **http://localhost:8000/docs**

## Using the API

### Health Check

```bash
curl http://localhost:8000/api/health
```

### Ask a Question

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is compound interest?",
    "k": 5
  }'
```

Response:
```json
{
  "answer": "Compound interest is...",
  "sources": [
    {
      "source": "financial-guide.txt",
      "chunk_id": 12,
      "score": 0.892,
      "text": "Compound interest refers to..."
    }
  ],
  "query": "What is compound interest?",
  "model": "gpt-4"
}
```

### Reload Knowledge Base

```bash
curl -X POST http://localhost:8000/api/reload_knowledge
```

This will:
1. Re-extract text from PDFs in `data/`
2. Rebuild embeddings
3. Update Qdrant index

## Troubleshooting

### Error: "OPENAI_API_KEY not found"

Make sure you've set the environment variable:
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

### Error: "Cannot connect to Qdrant"

Check if Qdrant is running:
```bash
docker ps | grep qdrant
```

If not running, start it:
```bash
docker run -p 6333:6333 qdrant/qdrant
```

### Error: "No text files found"

Make sure you've run the data extraction step:
```bash
cd app
python data_loader.py
```

### Rate Limit Errors

If you hit OpenAI rate limits, the pipeline includes delays between batches. For large document sets, consider:
- Reducing batch size in `rag_pipeline.py` (currently 20)
- Increasing delay between batches
- Using a higher-tier OpenAI account

## Configuration

### Change Chunk Size

Edit `app/rag_pipeline.py`:
```python
CHUNK_SIZE = 800       # Change to 1000 for larger chunks
CHUNK_OVERLAP = 100    # Adjust overlap as needed
```

### Change Embedding Model

Edit `app/rag_pipeline.py`:
```python
EMBEDDING_MODEL = "text-embedding-3-small"  # or "text-embedding-3-large"
```

### Change Chat Model

Edit `app/rag_pipeline.py`:
```python
CHAT_MODEL = "gpt-4"  # or "gpt-3.5-turbo" for faster/cheaper responses
```

## Production Considerations

Before deploying to production:

1. **Secure the `/api/reload_knowledge` endpoint** - Add authentication
2. **Set up proper CORS** - Restrict origins in `main.py`
3. **Add rate limiting** - Protect against abuse
4. **Use environment-specific configs** - Different settings for dev/staging/prod
5. **Monitor API usage** - Track OpenAI costs
6. **Set up logging** - Proper log aggregation
7. **Run as a service** - Use systemd, supervisor, or container orchestration
8. **Add health checks** - Monitor Qdrant and OpenAI connectivity

## Architecture Overview

```
User Question
     ↓
FastAPI (/api/chat)
     ↓
get_finance_answer()
     ↓
1. Generate query embedding (OpenAI)
     ↓
2. Search Qdrant for similar chunks
     ↓
3. Build context from results
     ↓
4. Send to GPT-4 with context
     ↓
5. Return answer + sources
```

## File Structure

```
moneymentor/
├── app/
│   ├── main.py              # FastAPI server
│   ├── rag_pipeline.py      # RAG implementation
│   ├── vectorstore.py       # Qdrant interface
│   ├── data_loader.py       # PDF/TXT extraction
│   └── data/
│       └── processed/       # Extracted text files
├── data/                    # Source PDFs/TXT files
├── requirements.txt
└── README.md
```

## Next Steps

1. Add more documents to `data/`
2. Customize the system prompt in `rag_pipeline.py`
3. Build a frontend (React, Vue, etc.)
4. Add user authentication
5. Implement conversation history
6. Add document upload via API

---

**MoneyMentor** - Your AI Financial Companion 💰

