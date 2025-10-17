# MoneyMentor - Testing Guide

Complete step-by-step guide to test the MoneyMentor RAG pipeline.

## Prerequisites Checklist

Before starting, ensure you have:
- [ ] Python 3.9+ installed
- [ ] Docker installed
- [ ] OpenAI API key
- [ ] PDF or TXT files in `data/` directory

---

## Step 1: Install Dependencies

```bash
cd /Users/amar.kulkarni/code/money-mentor-app/moneymentor
pip install -r requirements.txt
```

Expected output: All packages install successfully

---

## Step 2: Set Up Environment Variables

Create your `.env` file:

```bash
cat > .env << 'EOF'
OPENAI_API_KEY=sk-your-actual-key-here
QDRANT_URL=http://localhost:6333
EOF
```

Load the variables:

```bash
export $(cat .env | xargs)
```

Verify it's set:

```bash
echo $OPENAI_API_KEY
# Should display: sk-your-key...
```

---

## Step 3: Start Qdrant Vector Database

```bash
docker run -d -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage --name moneymentor-qdrant qdrant/qdrant
```

Verify it's running:

```bash
curl http://localhost:6333
# Should return: {"title":"qdrant - vector search engine",...}
```

Or check with docker:

```bash
docker ps | grep qdrant
# Should show the running container
```

---

## Step 4: Verify You Have Documents

Check if you have files to process:

```bash
ls -lh data/
```

You should see `.pdf` or `.txt` files. If not:

```bash
# The repo already has these files:
ls -lh data/*.pdf
# Should show: financialliteracy101.pdf, moneyandyouth.pdf
```

---

## Step 5: Extract Text from Documents

```bash
cd app
python data_loader.py
```

**Expected output:**
```
============================================================
MoneyMentor - Data Extraction Tool
============================================================

📂 Found 2 file(s) to process:
   - 2 PDF file(s)
   - 0 TXT file(s)

Processing: financialliteracy101.pdf
✅ Extracted X pages from financialliteracy101.pdf
💾 Saved processed text to data/processed/financialliteracy101.txt

Processing: moneyandyouth.pdf
✅ Extracted Y pages from moneyandyouth.pdf
💾 Saved processed text to data/processed/moneyandyouth.txt

✨ Processing complete! 2/2 files processed successfully.

📊 Summary:
   Total characters: XXX,XXX
   Total words: XX,XXX
   Output directory: /path/to/app/data/processed

✅ Successfully processed 2 file(s)!
```

Verify extracted files:

```bash
ls -lh data/processed/
# Should show .txt files
```

---

## Step 6: Build Embeddings and Index

This step will:
- Chunk the text
- Generate embeddings with OpenAI
- Store vectors in Qdrant

```bash
python rag_pipeline.py
```

**Expected output:**
```
============================================================
MoneyMentor - RAG Pipeline
============================================================

Loading knowledge base...
============================================================
Loading Knowledge Base into Vector Store
============================================================
🔌 Connecting to Qdrant at http://localhost:6333...
✅ Successfully connected to Qdrant
📦 Ensuring collection 'moneymentor_knowledge' exists...
📦 Creating collection 'moneymentor_knowledge' with vector size 1536...
✅ Collection 'moneymentor_knowledge' created successfully
📂 Found 2 text file(s) to process
✂️  Text splitter: chunk_size=800, overlap=100
🔌 Initializing OpenAI embeddings (text-embedding-3-small)...

📄 Processing: financialliteracy101.txt
   ✂️  Split into XX chunk(s)

📄 Processing: moneyandyouth.txt
   ✂️  Split into YY chunk(s)

✅ Created XXX total chunk(s) from 2 file(s)

🧮 Generating embeddings for XXX chunk(s)...
   (This may take a moment...)
   Processing batch 1/N
   Processing batch 2/N
   ...

✅ Generated XXX embedding vector(s)

💾 Upserting XXX vector(s) to Qdrant...
💾 Upserting XXX point(s) to 'moneymentor_knowledge'...
✅ Successfully upserted XXX point(s)

============================================================
✨ Knowledge Base Loading Complete!
============================================================
📊 Documents processed: 2
📊 Chunks created: XXX
📊 Vectors indexed: XXX
📊 Collection: moneymentor_knowledge
============================================================

✅ Knowledge base loaded successfully!
   Documents: 2
   Chunks: XXX
   Vectors: XXX
```

⏱️ **Time estimate:** 2-5 minutes depending on document size

---

## Step 7: Test Query via CLI

Now test if the RAG pipeline works:

```bash
python rag_pipeline.py --query "What is the importance of saving money?"
```

**Expected output:**
```
Testing query: 'What is the importance of saving money?'
------------------------------------------------------------
🔍 Processing query: 'What is the importance of saving money?'
🧮 Generating query embedding...
🔍 Searching for top 5 relevant chunks...
🔍 Found 5 result(s) in 'moneymentor_knowledge'
✅ Found 5 relevant chunk(s)
💬 Generating answer with GPT-4...
✅ Answer generated successfully

📝 Answer:
Saving money is crucial for several reasons. First, it provides financial security...
[GPT-4 generated answer based on your documents]

📚 Sources (5 found):
   1. moneyandyouth.txt (score: 0.876)
      Saving money is one of the most important financial habits...
   2. financialliteracy101.txt (score: 0.845)
      Financial experts recommend setting aside at least 20%...
   3. moneyandyouth.txt (score: 0.823)
      Building an emergency fund should be your first priority...
   4. financialliteracy101.txt (score: 0.812)
      Regular savings help you achieve your long-term goals...
   5. moneyandyouth.txt (score: 0.798)
      Understanding the power of compound interest...

🤖 Model: gpt-4
```

Try more queries:

```bash
# Try different questions
python rag_pipeline.py --query "How should I start investing?"
python rag_pipeline.py --query "What is compound interest?"
python rag_pipeline.py --query "How do I create a budget?"
```

---

## Step 8: Start the API Server

Open a new terminal (keep the current one open to see logs):

```bash
cd /Users/amar.kulkarni/code/money-mentor-app/moneymentor
export $(cat .env | xargs)
cd app
python main.py
```

**Expected output:**
```
INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
============================================================
MoneyMentor API Starting...
============================================================
API Version: 0.1.0
Docs available at: http://localhost:8000/docs
============================================================
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## Step 9: Test API Endpoints

Open another terminal for testing:

### Test 1: Health Check

```bash
curl http://localhost:8000/api/health
```

**Expected:** `{"ok":true}`

### Test 2: Ask a Question

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the importance of budgeting?",
    "k": 5
  }'
```

**Expected:** JSON response with answer and sources

```json
{
  "answer": "Budgeting is essential for...",
  "sources": [
    {
      "source": "financialliteracy101.txt",
      "chunk_id": 12,
      "score": 0.892,
      "text": "A budget helps you..."
    }
  ],
  "query": "What is the importance of budgeting?",
  "model": "gpt-4"
}
```

### Test 3: Reload Knowledge Base

```bash
curl -X POST http://localhost:8000/api/reload_knowledge
```

**Expected:** Success message with statistics

---

## Step 10: Interactive API Documentation

Open your browser and visit:

**http://localhost:8000/docs**

You'll see Swagger UI with all endpoints. Try:

1. Click on `POST /api/chat`
2. Click "Try it out"
3. Edit the request body:
   ```json
   {
     "question": "How do I save for retirement?",
     "k": 5
   }
   ```
4. Click "Execute"
5. See the response below

---

## Quick Test Script

I've created a test script for you:

```bash
cd /Users/amar.kulkarni/code/money-mentor-app/moneymentor
./test_app.sh
```

---

## Troubleshooting

### Issue: "OPENAI_API_KEY not found"

**Solution:**
```bash
export OPENAI_API_KEY="sk-your-key-here"
# Or reload .env
export $(cat .env | xargs)
```

### Issue: "Cannot connect to Qdrant"

**Solution:**
```bash
# Check if running
docker ps | grep qdrant

# If not running, start it
docker run -d -p 6333:6333 --name moneymentor-qdrant qdrant/qdrant

# Or restart existing container
docker start moneymentor-qdrant
```

### Issue: "No text files found"

**Solution:**
```bash
cd app
python data_loader.py
```

### Issue: "Port 8000 already in use"

**Solution:**
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn main:app --port 8001
```

### Issue: Rate limit errors from OpenAI

**Solution:**
- Wait a minute and try again
- Reduce batch size in `rag_pipeline.py` (line 206: `batch_size = 10`)
- Upgrade OpenAI tier

---

## Expected Results Summary

✅ **After extraction:** Text files in `app/data/processed/`  
✅ **After indexing:** Vectors in Qdrant collection  
✅ **CLI queries:** Get relevant answers with sources  
✅ **API health:** Returns `{"ok": true}`  
✅ **API chat:** Returns GPT-4 answers with sources  
✅ **API reload:** Successfully rebuilds index  
✅ **Interactive docs:** Swagger UI at `/docs`  

---

## Performance Benchmarks

- **Text extraction:** ~1 second per PDF page
- **Embedding generation:** ~2-3 seconds per 20 chunks
- **Query processing:** ~2-5 seconds total
- **Index rebuild:** ~2-5 minutes for 2 PDFs

---

## Next Steps

Once everything works:

1. ✅ Add more documents to `data/`
2. ✅ Customize the system prompt in `rag_pipeline.py`
3. ✅ Build a frontend
4. ✅ Add authentication
5. ✅ Deploy to production

---

**MoneyMentor** - Your AI Financial Companion 💰

