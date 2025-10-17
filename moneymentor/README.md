# MoneyMentor

**MoneyMentor** is an AI-powered financial advisory assistant that leverages Retrieval-Augmented Generation (RAG) to provide personalized financial guidance based on curated financial documents and best practices.

## Features

- 🤖 **RAG-based Q&A** - Ask financial questions, get AI-powered answers
- 📚 **Document Processing** - Automatic PDF/TXT extraction and chunking
- 🧮 **Smart Embeddings** - OpenAI text-embedding-3-small for semantic search
- 💾 **Vector Database** - Qdrant for fast similarity search
- 🤝 **GPT-4 Integration** - Context-aware answers with source citations
- 🔗 **FastAPI Backend** - RESTful API with automatic docs
- 🎨 **Modern React Frontend** - Coming soon (Phase 3)

## Project Structure

```
moneymentor/
├─ app/
│   ├─ main.py              # FastAPI application entry point
│   ├─ rag_pipeline.py      # RAG workflow implementation
│   ├─ vectorstore.py       # Qdrant vector database interface
│   ├─ data_loader.py       # Document loading and processing
│   ├─ agents/              # Agent system (Phase 2)
│   └─ frontend/            # React application
├─ data/                    # Curated financial documents (PDFs, texts)
├─ requirements.txt         # Python dependencies
└─ README.md               # This file
```

## Quick Start

### Prerequisites

- Python 3.9+
- Docker (for Qdrant)
- OpenAI API key

### Installation

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**
   ```bash
   export OPENAI_API_KEY="sk-your-key-here"
   export QDRANT_URL="http://localhost:6333"
   ```

3. **Start Qdrant**
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```

4. **Run quick start**
   ```bash
   ./quickstart.sh
   ```

   Or manually:
   ```bash
   cd app
   python data_loader.py     # Extract text from PDFs
   python rag_pipeline.py    # Build embeddings and index
   python main.py            # Start API server
   ```

📚 **For detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)**

## Usage

### API Endpoints

- **GET** `/api/health` - Health check
- **POST** `/api/chat` - Ask financial questions
- **POST** `/api/reload_knowledge` - Reload knowledge base

### Interactive Documentation

Visit http://localhost:8000/docs for Swagger UI

### Example: Ask a Question

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
  "answer": "Starting to invest is an excellent decision! Here are the key steps...",
  "sources": [
    {
      "source": "investing-guide.txt",
      "chunk_id": 5,
      "score": 0.892,
      "text": "When starting to invest..."
    }
  ],
  "query": "How should I start investing?",
  "model": "gpt-4"
}
```

### CLI Usage

Test queries directly:
```bash
cd app
python rag_pipeline.py --query "What is compound interest?"
```

## Development Roadmap

- [x] **Phase 1** - Project scaffolding and basic structure
- [x] **Phase 1.5** - Document ingestion and RAG pipeline
  - [x] PDF/TXT text extraction
  - [x] Text chunking with LangChain
  - [x] OpenAI embeddings integration
  - [x] Qdrant vector database setup
  - [x] GPT-4 answer generation
  - [x] API endpoints with FastAPI
- [ ] **Phase 2** - Multi-agent system implementation
- [ ] **Phase 3** - React frontend development
- [ ] **Phase 4** - Production deployment

## Contributing

Contributions are welcome! Please ensure all code follows the project's coding standards and includes appropriate tests.

## License

TBD

---

**MoneyMentor** - Your AI Financial Companion 💰✨

