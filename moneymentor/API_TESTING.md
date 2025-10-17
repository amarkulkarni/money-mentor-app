# MoneyMentor API Testing Guide

Quick reference for testing the MoneyMentor API endpoints.

## Starting the Server

```bash
cd moneymentor/app
python main.py
```

The server will start at `http://localhost:8000`

## API Endpoints

### 1. Health Check

**GET** `/api/health`

```bash
curl http://localhost:8000/api/health
```

Response:
```json
{
  "ok": true
}
```

### 2. Chat (Ask Financial Questions)

**POST** `/api/chat`

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How should I start investing?",
    "k": 5
  }'
```

Response:
```json
{
  "answer": "Placeholder: RAG pipeline not yet configured.",
  "sources": [],
  "query": "How should I start investing?",
  "model": "not-configured"
}
```

**Parameters:**
- `question` (required): Your financial question (1-1000 chars)
- `k` (optional): Number of relevant chunks to retrieve (1-20, default: 5)

### 3. Reload Knowledge Base

**POST** `/api/reload_knowledge`

```bash
curl -X POST http://localhost:8000/api/reload_knowledge
```

Response:
```json
{
  "reloaded": true,
  "message": "Successfully processed 2 file(s). Note: Embeddings rebuild not yet implemented.",
  "files_processed": 2
}
```

This endpoint:
- Scans `data/` directory for PDFs and TXT files
- Extracts text and saves to `app/data/processed/`
- Returns count of files processed

⚠️ **Dev Only:** This endpoint should be protected in production.

## Interactive API Documentation

FastAPI provides automatic interactive docs:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- View all endpoints
- See request/response schemas
- Test endpoints directly in the browser

## Testing with Python

```python
import requests

# Health check
response = requests.get("http://localhost:8000/api/health")
print(response.json())

# Ask a question
response = requests.post(
    "http://localhost:8000/api/chat",
    json={
        "question": "What is compound interest?",
        "k": 5
    }
)
print(response.json())

# Reload knowledge
response = requests.post("http://localhost:8000/api/reload_knowledge")
print(response.json())
```

## Testing with JavaScript/Fetch

```javascript
// Health check
fetch('http://localhost:8000/api/health')
  .then(r => r.json())
  .then(data => console.log(data));

// Ask a question
fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    question: "How do I budget effectively?",
    k: 5
  })
})
  .then(r => r.json())
  .then(data => console.log(data));
```

## CORS Configuration

The API allows requests from:
- `http://localhost:3000` (React)
- `http://localhost:5173` (Vite)
- `http://localhost:8000` (FastAPI)
- All origins (`*`) - Configure for production

## Error Responses

All endpoints return standard HTTP error codes:

**400 Bad Request** - Invalid input
```json
{
  "detail": "Validation error message"
}
```

**500 Internal Server Error** - Server error
```json
{
  "detail": "Error processing question: ..."
}
```

## Next Steps

1. Place PDF/TXT files in `moneymentor/data/`
2. Call `/api/reload_knowledge` to extract text
3. Implement embeddings in `rag_pipeline.py`
4. Test `/api/chat` with real questions

---

**MoneyMentor** - Your AI Financial Companion 💰

