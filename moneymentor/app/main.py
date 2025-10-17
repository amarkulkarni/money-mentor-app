"""
MoneyMentor - Main FastAPI Application

API Endpoints:
- GET  /api/health              - Health check
- POST /api/chat                - Ask financial questions (RAG + Calculator routing)
- POST /api/reload_knowledge    - Reload documents and rebuild index (dev only)
"""
import logging
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# Import local modules
from rag_pipeline import get_finance_answer, load_knowledge
from data_loader import DataLoader
from agents import run_calculation_query

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="MoneyMentor API",
    version="0.1.0",
    description="AI-powered financial advisory assistant with RAG capabilities"
)

# CORS configuration - allows frontend dev server and production origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # React dev server
        "http://localhost:5173",      # Vite dev server
        "http://localhost:8000",      # FastAPI server
        "*"                           # Allow all (configure for production)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Request/Response Models
# ============================================================================

class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User's financial question"
    )
    k: Optional[int] = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of relevant chunks to retrieve"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "How should I start investing?",
                "k": 5
            }
        }


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    answer: str
    sources: list
    query: str
    model: str
    tool: str = "rag"  # "calculator" or "rag"


class ReloadResponse(BaseModel):
    """Response model for reload_knowledge endpoint"""
    reloaded: bool
    message: str
    files_processed: Optional[int] = 0


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    
    Returns:
        {"ok": true} if service is running
    """
    return {"ok": True}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Ask a financial question and get an AI-powered answer.
    
    This endpoint uses intelligent routing to:
    1. Detect calculation queries → Financial Calculator Agent
    2. General questions → RAG (Retrieval-Augmented Generation) pipeline
    
    Args:
        request: ChatRequest with user's question
        
    Returns:
        ChatResponse with answer, sources, and tool used
        
    Example:
        POST /api/chat
        {
            "question": "If I invest $500 monthly at 7% for 20 years?",
            "k": 5
        }
    """
    try:
        logger.info(f"Received chat request: '{request.question}'")
        
        # Intent detection: Check if this is a calculation query
        question_lower = request.question.lower()
        calculation_keywords = [
            "invest", "investing", "monthly", "per month", 
            "compound", "annuity", "save", "saving",
            "how much will i have", "future value", "per year"
        ]
        
        is_calculation = any(keyword in question_lower for keyword in calculation_keywords)
        
        # Route to appropriate tool
        if is_calculation:
            logger.info("🧮 Routing to calculator agent")
            
            # Try calculator agent first
            calc_result = run_calculation_query(request.question)
            
            if calc_result['success']:
                # Calculator succeeded - return formatted result with MoneyMentor branding
                answer_with_branding = (
                    f"💰 **MoneyMentor Calculator**\n\n"
                    f"{calc_result['explanation']}"
                )
                
                logger.info(f"✅ Calculator agent successful: ${calc_result['result']:,.2f}")
                
                return ChatResponse(
                    answer=answer_with_branding,
                    sources=[{
                        'source': 'financial_calculator',
                        'text': f"Calculated with parameters: {calc_result['parameters']}",
                        'relevance_score': 1.0
                    }],
                    query=request.question,
                    model='calculator_agent',
                    tool='calculator'
                )
            else:
                # Calculator couldn't parse - fall back to RAG
                logger.info("⚠️  Calculator parsing failed, falling back to RAG")
        
        # Default: Use RAG pipeline
        logger.info("📚 Routing to RAG pipeline")
        result = get_finance_answer(
            query=request.question,
            k=request.k
        )
        
        logger.info(f"✅ RAG answer generated with {len(result.get('sources', []))} sources")
        
        return ChatResponse(
            answer=result["answer"],
            sources=result.get("sources", []),
            query=result.get("query", request.question),
            model=result.get("model", "gpt-4"),
            tool='rag'
        )
        
    except Exception as e:
        logger.error(f"❌ Error processing chat request: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )


@app.post("/api/reload_knowledge", response_model=ReloadResponse)
async def reload_knowledge():
    """
    Reload knowledge base from documents (Dev/Admin endpoint).
    
    This endpoint:
    1. Re-extracts text from PDFs/TXT files in data/
    2. Saves processed text to app/data/processed/
    3. Rebuilds embeddings and vector index in Qdrant
    
    ⚠️  Note: This is a development endpoint. In production, this should be:
    - Protected with authentication
    - Rate-limited
    - Run as a background job
    
    Returns:
        ReloadResponse with status and file count
        
    Example:
        POST /api/reload_knowledge
        {}
    """
    try:
        logger.info("Starting knowledge base reload...")
        
        # Step 1: Extract text from source documents
        logger.info("Step 1: Extracting text from documents...")
        loader = DataLoader(
            data_dir="../data",
            output_dir="./data/processed"
        )
        
        results = loader.process_all_files()
        
        if not results:
            logger.warning("⚠️  No files were processed")
            return ReloadResponse(
                reloaded=False,
                message="No files found or processed. Check data/ directory.",
                files_processed=0
            )
        
        logger.info(f"✅ Extracted text from {len(results)} file(s)")
        
        # Step 2: Load knowledge base (chunk, embed, index)
        logger.info("Step 2: Building embeddings and indexing...")
        index_result = load_knowledge(processed_dir="./data/processed")
        
        if index_result["success"]:
            message = (
                f"Successfully reloaded knowledge base! "
                f"Processed {index_result['documents_processed']} document(s), "
                f"created {index_result['chunks_created']} chunk(s), "
                f"indexed {index_result['vectors_indexed']} vector(s)."
            )
            logger.info(f"✅ {message}")
            
            return ReloadResponse(
                reloaded=True,
                message=message,
                files_processed=len(results)
            )
        else:
            error_msg = index_result.get("error", "Unknown error during indexing")
            logger.error(f"❌ Indexing failed: {error_msg}")
            
            return ReloadResponse(
                reloaded=False,
                message=f"Text extraction succeeded but indexing failed: {error_msg}",
                files_processed=len(results)
            )
            
    except Exception as e:
        logger.error(f"Error reloading knowledge base: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error reloading knowledge: {str(e)}"
        )


# ============================================================================
# Static File Serving (Frontend)
# ============================================================================

# Mount static files for frontend after API routes
# This should be last to avoid catching API routes
frontend_dist = Path(__file__).parent / "frontend" / "dist"
if frontend_dist.exists():
    logger.info(f"✅ Mounting frontend from {frontend_dist}")
    app.mount(
        "/",
        StaticFiles(directory=str(frontend_dist), html=True),
        name="frontend"
    )
    logger.info("✅ Frontend available at http://localhost:8000")
else:
    logger.warning(f"⚠️  Frontend dist not found at {frontend_dist}")
    logger.warning(f"   Run: cd frontend && npm run build")
    
    # Fallback root endpoint if frontend not built
    @app.get("/")
    async def root():
        """Root endpoint - serves API info when frontend not built"""
        return {
            "app": "MoneyMentor API",
            "version": "0.1.0",
            "status": "running",
            "docs": "/docs",
            "message": "Frontend not built. Run: cd frontend && npm run build",
            "endpoints": {
                "health": "GET /api/health",
                "chat": "POST /api/chat",
                "reload": "POST /api/reload_knowledge"
            }
        }


# ============================================================================
# Startup/Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("=" * 60)
    logger.info("MoneyMentor API Starting...")
    logger.info("=" * 60)
    logger.info(f"API Version: {app.version}")
    logger.info(f"Docs available at: http://localhost:8000/docs")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("MoneyMentor API shutting down...")


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting MoneyMentor API server...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

