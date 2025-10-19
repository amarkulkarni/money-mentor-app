# MoneyMentor

**MoneyMentor** is an AI-powered financial advisory assistant that leverages Retrieval-Augmented Generation (RAG) to provide personalized financial guidance based on curated financial documents and best practices.

## Features

- 🤖 **RAG-based Q&A** - Ask financial questions, get AI-powered answers
- 🧮 **Financial Calculator Agent** - Instant investment calculations (FV, compound interest)
- 🎯 **Intelligent Routing** - Automatic intent detection (calculator vs RAG vs greeting)
- 📚 **Document Processing** - Automatic PDF/TXT extraction and chunking
- 🔍 **Smart Embeddings** - OpenAI text-embedding-3-small for semantic search
- 💾 **Vector Database** - Qdrant for fast similarity search
- 🤝 **GPT-4 Integration** - Context-aware answers with source citations
- 🔗 **FastAPI Backend** - RESTful API with automatic docs
- 🎨 **React Frontend** - Modern chat interface with Tailwind CSS

## Project Structure

```
moneymentor/
├─ app/
│   ├─ main.py              # FastAPI application with intelligent routing
│   ├─ rag_pipeline.py      # RAG workflow implementation
│   ├─ vectorstore.py       # Qdrant vector database interface
│   ├─ data_loader.py       # Document loading and processing
│   ├─ evaluation.py        # RAGAS evaluation placeholder (Phase 2)
│   ├─ agents/              # Agent system
│   │   ├─ finance_calculator_agent.py  # Investment calculator
│   │   └─ __init__.py
│   └─ frontend/            # React + TypeScript + Tailwind UI
├─ data/                    # Curated financial documents (PDFs, texts)
├─ requirements.txt         # Python dependencies
├─ README.md               # This file
└─ SETUP_GUIDE.md          # Detailed setup instructions
```

## Quick Start

### Prerequisites

- Python 3.9+
- Qdrant (Docker or standalone binary)
- OpenAI API key

### Installation

1. **Clone and navigate to project**
   ```bash
   cd moneymentor
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   
   Create a `.env` file:
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` and add your keys:
   ```
   OPENAI_API_KEY=sk-your-openai-key-here
   QDRANT_URL=http://localhost:6333
   # QDRANT_API_KEY=your-key  # Optional, for Qdrant Cloud
   ```
   
   Or export directly:
   ```bash
   export OPENAI_API_KEY="sk-your-key-here"
   export QDRANT_URL="http://localhost:6333"
   ```

5. **Start Qdrant**
   
   **Option A: Docker (Recommended)**
   ```bash
   docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
   ```
   
   **Option B: Standalone Binary**
   ```bash
   ./setup_qdrant.sh  # Downloads and starts Qdrant binary
   # Or manually:
   ./qdrant &
   ```

6. **Process documents and build index**
   ```bash
   cd app
   python data_loader.py      # Extract text from PDFs in data/
   python rag_pipeline.py     # Build embeddings and index
   ```

7. **Start the server**
   
   **Option A: Using uvicorn (recommended for development)**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   **Option B: Direct Python**
   ```bash
   python main.py
   ```
   
   **Option C: Using dev script (builds frontend + starts server)**
   ```bash
   cd ..  # Back to moneymentor/
   ./dev.sh
   ```

8. **Access the application**
   - Frontend: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/api/health

📚 **For detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)**

---

### Adding New Documents

To add your own financial documents:

1. **Add files to data/ folder**
   ```bash
   cp your-financial-guide.pdf data/
   cp investment-tips.txt data/
   ```

2. **Extract text from new documents**
   ```bash
   cd app
   python data_loader.py
   ```
   
   This will:
   - Scan `data/` for .pdf and .txt files
   - Extract text using PyMuPDF
   - Save processed text to `app/data/processed/`

3. **Rebuild the index**
   ```bash
   python rag_pipeline.py
   ```
   
   This will:
   - Chunk the processed text (800 chars, 100 overlap)
   - Generate embeddings with OpenAI
   - Upsert to Qdrant vector database

4. **Restart the server or reload**
   
   **Option A: Restart server**
   ```bash
   # Stop server (Ctrl+C), then restart
   python -m uvicorn app.main:app --reload
   ```
   
   **Option B: Use reload endpoint (no restart needed)**
   ```bash
   curl -X POST http://localhost:8000/api/reload_knowledge
   ```

**Supported formats:** PDF, TXT  
**Recommended:** Use well-structured documents with clear sections for best results.

## Usage

### API Endpoints

- **GET** `/api/health` - Health check
- **POST** `/api/chat` - Ask financial questions with intelligent routing
  - Automatically routes to calculator, RAG, or direct response
  - Returns answer with sources and tool used
- **POST** `/api/reload_knowledge` - Reload knowledge base (dev endpoint)

### Interactive Documentation

Visit http://localhost:8000/docs for Swagger UI with interactive API testing.

### Example: Ask a Question

**Financial Question (RAG):**
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
      "source": "financialliteracy101.txt",
      "chunk_id": 5,
      "score": 0.892,
      "text": "When starting to invest..."
    }
  ],
  "query": "How should I start investing?",
  "model": "gpt-4",
  "tool": "rag"
}
```

**Investment Calculation (Calculator Agent):**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "If I invest $500 monthly at 7% for 20 years, how much will I have?"
  }'
```

Response:
```json
{
  "answer": "💰 **MoneyMentor Calculator**\n\nInvesting $500.00/month at 7.0% annual return for 20 years:\n• Total contributions: $120,000.00\n• Interest earned: $140,463.33\n• Final value: $260,463.33\nYour money will grow 2.17x through compound interest!",
  "sources": [
    {
      "source": "financial_calculator",
      "text": "Calculated with parameters: {'monthly_contrib': 500.0, 'annual_rate': 7.0, 'years': 20}",
      "relevance_score": 1.0
    }
  ],
  "query": "If I invest $500 monthly at 7% for 20 years, how much will I have?",
  "model": "calculator_agent",
  "tool": "calculator"
}
```

### CLI Usage

**Test RAG pipeline:**
```bash
cd app
python rag_pipeline.py --query "What is compound interest?"
```

**Test calculator agent:**
```bash
python agents/finance_calculator_agent.py
# Or test specific calculation:
python -c "from agents import run_calculation_query; print(run_calculation_query('$500 monthly at 7% for 20 years'))"
```

**Run evaluation (placeholder):**
```bash
python -m app.evaluation --test-set data/test_set.jsonl
# Or create sample test set:
python -m app.evaluation --create-sample
```

## Development Roadmap

- [x] **Phase 1** - Core RAG Pipeline ✅
  - [x] Project scaffolding and basic structure
  - [x] PDF/TXT text extraction with PyMuPDF
  - [x] Text chunking with LangChain (800 chars, 100 overlap)
  - [x] OpenAI embeddings integration (text-embedding-3-small)
  - [x] Qdrant vector database setup and management
  - [x] GPT-4 answer generation with source citations
  - [x] FastAPI backend with API endpoints
  - [x] React frontend with Tailwind CSS
  
- [x] **Phase 2** - Agent System (Partial) 🚧
  - [x] Financial calculator agent (FV, compound interest)
  - [x] Intelligent intent routing (calculator/RAG/greeting)
  - [x] Natural language query parsing
  - [x] Evaluation framework placeholder (RAGAS)
  - [ ] **Upcoming**: Additional financial agents
    - [ ] Loan/mortgage calculator agent
    - [ ] Budget planner agent
    - [ ] Retirement calculator agent
  - [ ] **Upcoming**: External tool integration
    - [ ] Brave Search API for real-time financial data
    - [ ] Tavily API for news and market updates
    - [ ] Stock/crypto price APIs
  - [ ] **Upcoming**: Advanced routing
    - [ ] LLM-based intent classification
    - [ ] Multi-agent orchestration
    - [ ] Tool selection and chaining
  - [ ] **Upcoming**: Evaluation
    - [ ] RAGAS metrics implementation
    - [ ] Automated testing pipeline
    - [ ] Performance benchmarking
    
- [ ] **Phase 3** - Production Enhancements 🔮
  - [ ] User authentication and sessions
  - [ ] Conversation history and memory
  - [ ] User feedback collection
  - [ ] A/B testing framework
  - [ ] Rate limiting and caching
  - [ ] Monitoring and analytics
  
- [ ] **Phase 4** - Deployment 🚀
  - [ ] Docker containerization
  - [ ] CI/CD pipeline
  - [ ] Cloud deployment (AWS/GCP/Azure)
  - [ ] Load balancing and scaling
  - [ ] Security hardening
  - [ ] Documentation and API versioning

### Phase 2 Notes: Future Agent Integrations

**Brave Search Integration** (Planned)
- Real-time web search for current financial news
- Market data and stock prices
- Regulatory updates and policy changes
- Use case: "What's the current inflation rate?"

**Tavily API Integration** (Planned)
- Specialized financial and business news
- Company research and analysis
- Economic indicators and reports
- Use case: "Latest news about federal interest rates"

**Implementation Strategy:**
1. Add web search agent module
2. Implement query classification (local knowledge vs real-time data)
3. Create fallback mechanism (local → web search)
4. Add source attribution for web results
5. Implement result caching for cost optimization

## Contributing

Contributions are welcome! Please ensure all code follows the project's coding standards and includes appropriate tests.

## License

TBD

---

**MoneyMentor** - Your AI Financial Companion 💰✨

