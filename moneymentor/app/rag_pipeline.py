"""
MoneyMentor - RAG Pipeline
Handles retrieval-augmented generation workflow

This module orchestrates the RAG (Retrieval-Augmented Generation) pipeline:
1. Load and chunk documents
2. Generate embeddings (using LangChain + OpenAI)
3. Store in vector database (Qdrant)
4. Retrieve relevant context for user queries
5. Generate answers using LLM with retrieved context
"""
import os
import logging
import time
from typing import List, Dict, Any, Optional
from pathlib import Path

# LangChain imports
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_community.vectorstores import Qdrant

# Qdrant imports
from qdrant_client.models import PointStruct

# LangSmith tracking
try:
    from langsmith import Client
    langsmith_client = Client()
    HAS_LANGSMITH = True
except ImportError:
    HAS_LANGSMITH = False
    langsmith_client = None
    logger.warning("LangSmith not available - tracking will be disabled")

# Import local modules
from data_loader import DataLoader
from vectorstore import (
    get_qdrant_client,
    ensure_collection,
    upsert_points,
    search_points
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
COLLECTION_NAME = "moneymentor_knowledge"
VECTOR_SIZE = 1536  # OpenAI text-embedding-3-small dimension
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"  # Fast and cost-effective model


def load_knowledge(
    processed_dir: str = "./data/processed",
    collection_name: str = COLLECTION_NAME,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
    force_rebuild: bool = False
) -> Dict[str, Any]:
    """
    Load knowledge base: read processed text files, chunk, embed, and index in Qdrant.
    
    This function orchestrates the complete indexing pipeline:
    1. Read text files from processed_dir (app/data/processed/*.txt)
    2. Chunk text using CharacterTextSplitter
    3. Generate embeddings using OpenAI text-embedding-3-small
    4. Store embeddings in Qdrant vector database
    
    Args:
        processed_dir: Directory containing processed text files
        collection_name: Name of Qdrant collection to create/use
        chunk_size: Maximum size of text chunks (characters)
        chunk_overlap: Overlap between consecutive chunks (characters)
        force_rebuild: If True, delete and rebuild collection even if it exists
        
    Returns:
        Dictionary with indexing statistics
    """
    logger.info("=" * 60)
    logger.info("Loading Knowledge Base into Vector Store")
    logger.info("=" * 60)
    
    try:
        # Check for OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("❌ OPENAI_API_KEY not found in environment")
            return {
                "success": False,
                "error": "OPENAI_API_KEY not set",
                "documents_processed": 0,
                "chunks_created": 0,
                "vectors_indexed": 0
            }
        
        # Check Qdrant connection
        client = get_qdrant_client()
        if not client:
            logger.error("❌ Cannot connect to Qdrant")
            return {
                "success": False,
                "error": "Qdrant connection failed",
                "documents_processed": 0,
                "chunks_created": 0,
                "vectors_indexed": 0
            }
        
        # Ensure collection exists
        logger.info(f"📦 Ensuring collection '{collection_name}' exists...")
        if not ensure_collection(collection_name, VECTOR_SIZE):
            return {
                "success": False,
                "error": "Failed to create collection",
                "documents_processed": 0,
                "chunks_created": 0,
                "vectors_indexed": 0
            }
        
        # Find all processed text files
        processed_path = Path(processed_dir)
        if not processed_path.exists():
            logger.error(f"❌ Processed directory not found: {processed_dir}")
            return {
                "success": False,
                "error": f"Directory not found: {processed_dir}",
                "documents_processed": 0,
                "chunks_created": 0,
                "vectors_indexed": 0
            }
        
        txt_files = list(processed_path.glob("*.txt"))
        if not txt_files:
            logger.warning(f"⚠️  No .txt files found in {processed_dir}")
            return {
                "success": False,
                "error": "No text files found",
                "documents_processed": 0,
                "chunks_created": 0,
                "vectors_indexed": 0
            }
        
        logger.info(f"📂 Found {len(txt_files)} text file(s) to process")
        
        # Initialize text splitter
        text_splitter = CharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separator="\n"
        )
        logger.info(f"✂️  Text splitter: chunk_size={chunk_size}, overlap={chunk_overlap}")
        
        # Initialize OpenAI embeddings
        logger.info(f"🔌 Initializing OpenAI embeddings ({EMBEDDING_MODEL})...")
        embeddings = OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            openai_api_key=api_key
        )
        
        # Process each file
        all_chunks = []
        documents_processed = 0
        
        for file_path in txt_files:
            try:
                logger.info(f"\n📄 Processing: {file_path.name}")
                
                # Read file
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                if not text.strip():
                    logger.warning(f"   ⚠️  Empty file, skipping")
                    continue
                
                # Split into chunks
                chunks = text_splitter.split_text(text)
                logger.info(f"   ✂️  Split into {len(chunks)} chunk(s)")
                
                # Create document chunks with metadata
                for i, chunk_text in enumerate(chunks):
                    all_chunks.append({
                        "text": chunk_text,
                        "source": file_path.name,
                        "chunk_id": i
                    })
                
                documents_processed += 1
                
            except Exception as e:
                logger.error(f"   ❌ Error processing {file_path.name}: {e}")
                continue
        
        if not all_chunks:
            logger.warning("⚠️  No chunks created from any files")
            return {
                "success": False,
                "error": "No chunks created",
                "documents_processed": documents_processed,
                "chunks_created": 0,
                "vectors_indexed": 0
            }
        
        logger.info(f"\n✅ Created {len(all_chunks)} total chunk(s) from {documents_processed} file(s)")
        
        # Generate embeddings and create points
        logger.info(f"\n🧮 Generating embeddings for {len(all_chunks)} chunk(s)...")
        logger.info("   (This may take a moment...)")
        
        points = []
        batch_size = 20  # Process in batches to handle rate limits
        
        for i in range(0, len(all_chunks), batch_size):
            batch = all_chunks[i:i + batch_size]
            batch_texts = [chunk["text"] for chunk in batch]
            
            try:
                # Generate embeddings for batch
                logger.info(f"   Processing batch {i // batch_size + 1}/{(len(all_chunks) + batch_size - 1) // batch_size}")
                vectors = embeddings.embed_documents(batch_texts)
                
                # Create PointStruct objects
                for j, (chunk, vector) in enumerate(zip(batch, vectors)):
                    point_id = i + j
                    points.append(PointStruct(
                        id=point_id,
                        vector=vector,
                        payload={
                            "text": chunk["text"],
                            "source": chunk["source"],
                            "chunk_id": chunk["chunk_id"]
                        }
                    ))
                
                # Small delay to avoid rate limits
                if i + batch_size < len(all_chunks):
                    time.sleep(0.5)
                    
            except Exception as e:
                logger.error(f"   ❌ Error generating embeddings for batch: {e}")
                # Continue with next batch
                continue
        
        if not points:
            logger.error("❌ No embeddings generated")
            return {
                "success": False,
                "error": "Embedding generation failed",
                "documents_processed": documents_processed,
                "chunks_created": len(all_chunks),
                "vectors_indexed": 0
            }
        
        logger.info(f"✅ Generated {len(points)} embedding vector(s)")
        
        # Upsert to Qdrant in batches to avoid timeouts
        logger.info(f"\n💾 Upserting {len(points)} vector(s) to Qdrant...")
        upsert_batch_size = 100  # Batch size for upsert operations
        vectors_indexed = 0
        
        for i in range(0, len(points), upsert_batch_size):
            batch = points[i:i + upsert_batch_size]
            batch_num = (i // upsert_batch_size) + 1
            total_batches = (len(points) + upsert_batch_size - 1) // upsert_batch_size
            
            logger.info(f"   Upserting batch {batch_num}/{total_batches} ({len(batch)} vectors)...")
            
            if not upsert_points(collection_name, batch):
                logger.error(f"   ❌ Failed to upsert batch {batch_num}")
                return {
                    "success": False,
                    "error": f"Failed to upsert vectors at batch {batch_num}",
                    "documents_processed": documents_processed,
                    "chunks_created": len(all_chunks),
                    "vectors_indexed": vectors_indexed
                }
            
            vectors_indexed += len(batch)
            logger.info(f"   ✅ Batch {batch_num} complete ({vectors_indexed}/{len(points)} total)")
        
        if vectors_indexed != len(points):
            return {
                "success": False,
                "error": "Incomplete upsert",
                "documents_processed": documents_processed,
                "chunks_created": len(all_chunks),
                "vectors_indexed": vectors_indexed
            }
        
        logger.info("")
        logger.info("=" * 60)
        logger.info("✨ Knowledge Base Loading Complete!")
        logger.info("=" * 60)
        logger.info(f"📊 Documents processed: {documents_processed}")
        logger.info(f"📊 Chunks created: {len(all_chunks)}")
        logger.info(f"📊 Vectors indexed: {vectors_indexed}")
        logger.info(f"📊 Collection: {collection_name}")
        logger.info("=" * 60)
        
        return {
            "success": True,
            "documents_processed": documents_processed,
            "chunks_created": len(all_chunks),
            "vectors_indexed": vectors_indexed,
            "collection_name": collection_name
        }
        
    except Exception as e:
        logger.error(f"❌ Error in load_knowledge: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "documents_processed": 0,
            "chunks_created": 0,
            "vectors_indexed": 0
        }


def get_base_retriever(collection_name: str = COLLECTION_NAME, k: int = 5):
    """
    Create a base similarity search retriever.
    
    Args:
        collection_name: Qdrant collection name
        k: Number of documents to retrieve
        
    Returns:
        Base retriever using similarity search
    """
    logger.info("🔍 Using Base Retriever (similarity search)")
    
    # Get Qdrant client and embeddings
    client = get_qdrant_client()
    api_key = os.getenv("OPENAI_API_KEY")
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=api_key)
    
    # Create Qdrant vectorstore
    # Specify content_payload_key="text" to match our stored data format
    # Our data has source/chunk_id at top level of payload, not nested
    vectorstore = Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embeddings,
        content_payload_key="text"
    )
    
    return vectorstore.as_retriever(search_kwargs={"k": k})


def get_advanced_retriever(collection_name: str = COLLECTION_NAME, k: int = 5):
    """
    Create an advanced MultiQueryRetriever for better query expansion.
    
    This retriever generates multiple query variations to improve retrieval quality.
    
    Args:
        collection_name: Qdrant collection name
        k: Number of documents to retrieve per query variation
        
    Returns:
        Advanced MultiQuery retriever
    """
    logger.info("🚀 Using Advanced Retriever (MultiQuery with expansion)")
    
    # Get Qdrant client and embeddings
    client = get_qdrant_client()
    api_key = os.getenv("OPENAI_API_KEY")
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=api_key)
    
    # Create Qdrant vectorstore
    # Specify content_payload_key="text" to match our stored data format
    # Our data has source/chunk_id at top level of payload, not nested
    vectorstore = Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embeddings,
        content_payload_key="text"
    )
    
    # Create LLM for query generation
    llm = ChatOpenAI(
        model=CHAT_MODEL,
        temperature=0.7,
        openai_api_key=api_key
    )
    
    # Create base retriever
    base_retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    
    # Wrap with MultiQueryRetriever for query expansion
    advanced_retriever = MultiQueryRetriever.from_llm(
        retriever=base_retriever,
        llm=llm
    )
    
    logger.info("   ✓ MultiQuery will generate query variations for better retrieval")
    
    return advanced_retriever


def get_retriever(mode: str = "base", collection_name: str = COLLECTION_NAME, k: int = 5):
    """
    Get retriever based on mode selection.
    
    Args:
        mode: "base" for similarity search, "advanced" for MultiQuery
        collection_name: Qdrant collection name
        k: Number of documents to retrieve
        
    Returns:
        Configured retriever
    """
    if mode == "advanced":
        return get_advanced_retriever(collection_name, k)
    return get_base_retriever(collection_name, k)


def get_finance_answer(
    query: str,
    k: int = 5,
    collection_name: str = COLLECTION_NAME,
    mode: str = "base",
    return_context: bool = False
) -> Dict[str, Any]:
    """
    Get an answer to a financial question using RAG pipeline.
    
    This function implements the query workflow:
    1. Generate embedding for user query (or use MultiQuery for expansion)
    2. Search Qdrant for k most similar document chunks
    3. Build context from retrieved chunks
    4. Generate answer using GPT-4o-mini with context
    5. Log to LangSmith for tracking and comparison
    
    Args:
        query: User's financial question
        k: Number of relevant chunks to retrieve
        collection_name: Qdrant collection to search
        mode: "base" for similarity search, "advanced" for MultiQuery expansion
        return_context: If True, return contexts for evaluation
        
    Returns:
        Dictionary containing answer and sources
    """
    logger.info(f"🔍 Processing query: '{query}'")
    logger.info(f"   Mode: {mode.upper()}")
    
    try:
        # Check for OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("❌ OPENAI_API_KEY not found in environment")
            return {
                "answer": "Error: OpenAI API key not configured. Please set OPENAI_API_KEY environment variable.",
                "sources": [],
                "query": query,
                "model": "error",
                "mode": mode
            }
        
        # Get retriever based on mode
        retriever = get_retriever(mode=mode, collection_name=collection_name, k=k)
        
        # Retrieve relevant documents
        logger.info(f"🔍 Retrieving documents using {mode} retriever...")
        docs = retriever.get_relevant_documents(query)
        
        if not docs:
            logger.warning("⚠️  No relevant context found in knowledge base")
            answer = "I apologize, but I couldn't find relevant information in my knowledge base to answer your question. Please ensure the knowledge base has been loaded, or try rephrasing your question."
            
            if HAS_LANGSMITH:
                try:
                    langsmith_client.create_run(
                        name=f"MoneyMentor_RAG_{mode}",
                        run_type="chain",
                        inputs={"query": query, "mode": mode},
                        outputs={"answer": answer, "num_docs": 0},
                        tags=["moneymentor", "rag", f"{mode}_retriever", "no_results"]
                    )
                except Exception as e:
                    logger.warning(f"LangSmith logging failed: {e}")
            
            return {
                "answer": answer,
                "sources": [],
                "query": query,
                "model": CHAT_MODEL,
                "mode": mode
            }
        
        logger.info(f"✅ Found {len(docs)} relevant document(s)")
        
        # Extract context and prepare sources
        context_chunks = []
        sources = []
        
        for i, doc in enumerate(docs):
            chunk_text = doc.page_content
            metadata = doc.metadata
            source_file = metadata.get("source", "unknown")
            chunk_id = metadata.get("chunk_id", 0)
            
            context_chunks.append(f"[Source {i+1}: {source_file}]\n{chunk_text}")
            sources.append({
                "source": source_file,
                "chunk_id": chunk_id,
                "score": metadata.get("score", 0.0),
                "text": chunk_text[:200] + "..." if len(chunk_text) > 200 else chunk_text
            })
        
        # Build context string
        context = "\n\n---\n\n".join(context_chunks)
        
        # Create prompt with context
        logger.info("💬 Generating answer with GPT-4o-mini...")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are MoneyMentor, a knowledgeable and friendly financial advisor assistant. 
Your role is to provide clear, accurate, and helpful financial advice based on the provided context.

Guidelines:
- Use the context below to answer questions accurately
- Provide practical, actionable advice when appropriate
- If the context doesn't contain enough information, say so honestly
- Use a warm, professional, and encouraging tone
- Break down complex concepts into easy-to-understand explanations
- When relevant, provide examples or analogies

Context from knowledge base:
{context}

Remember: You are MoneyMentor, here to help people make informed financial decisions."""),
            ("user", "{question}")
        ])
        
        # Initialize LLM
        llm = ChatOpenAI(
            model=CHAT_MODEL,
            temperature=0.7,
            openai_api_key=api_key
        )
        
        # Generate answer
        chain = prompt | llm
        response = chain.invoke({
            "context": context,
            "question": query
        })
        
        answer_text = response.content
        
        logger.info("✅ Answer generated successfully")
        
        # Log to LangSmith
        if HAS_LANGSMITH:
            try:
                langsmith_client.create_run(
                    name=f"MoneyMentor_RAG_{mode}",
                    run_type="chain",
                    inputs={
                        "query": query,
                        "mode": mode,
                        "k": k,
                        "collection": collection_name
                    },
                    outputs={
                        "answer": answer_text,
                        "num_docs": len(docs),
                        "num_sources": len(sources)
                    },
                    extra={
                        "context": context[:500] + "..." if len(context) > 500 else context,
                        "sources": sources,
                        "metadata": {
                            "retriever_mode": mode,
                            "model": CHAT_MODEL,
                            "embedding_model": EMBEDDING_MODEL,
                            "docs_retrieved": len(docs)
                        }
                    },
                    tags=["moneymentor", "rag", f"{mode}_retriever"]
                )
                logger.info(f"   📊 Logged to LangSmith (mode: {mode})")
            except Exception as e:
                logger.warning(f"   ⚠️  LangSmith logging failed: {e}")
        
        result = {
            "answer": answer_text,
            "sources": sources,
            "query": query,
            "model": CHAT_MODEL,
            "mode": mode
        }
        
        # Add contexts for evaluation if requested
        if return_context:
            result["contexts"] = [doc.page_content for doc in docs]
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Error in get_finance_answer: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            "answer": f"I apologize, but I encountered an error while processing your question: {str(e)}",
            "sources": [],
            "query": query,
            "model": "error",
            "mode": mode
        }


# Backward compatibility aliases
def build_embeddings_and_index(**kwargs) -> Dict[str, Any]:
    """Alias for load_knowledge() - backward compatibility"""
    return load_knowledge(**kwargs)


# Legacy RAGPipeline class for backward compatibility
class RAGPipeline:
    """
    RAG Pipeline class-based interface (legacy).
    
    For new code, prefer using the functional API:
    - load_knowledge()
    - get_finance_answer()
    """
    
    def __init__(
        self,
        collection_name: str = COLLECTION_NAME
    ):
        """Initialize RAG pipeline components"""
        self.collection_name = collection_name
        self.client = get_qdrant_client()
        logger.info(f"Initialized RAGPipeline with collection '{collection_name}'")
    
    async def query(self, user_query: str, k: int = 5, **kwargs) -> Dict[str, Any]:
        """
        Process a user query through the RAG pipeline
        
        Args:
            user_query: The user's question or prompt
            k: Number of relevant chunks to retrieve
            **kwargs: Additional parameters
            
        Returns:
            Dictionary containing response and metadata
        """
        # Wrapper around functional API
        return get_finance_answer(user_query, k=k, collection_name=self.collection_name)
    
    def build_index(self, **kwargs) -> Dict[str, Any]:
        """Build embeddings and index documents"""
        return load_knowledge(collection_name=self.collection_name, **kwargs)


if __name__ == "__main__":
    """
    CLI tool for loading knowledge base and testing queries
    
    Usage:
        python rag_pipeline.py                    # Load knowledge base
        python rag_pipeline.py --query "question" # Test a query
    """
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="MoneyMentor RAG Pipeline")
    parser.add_argument("--query", type=str, help="Test query to run")
    parser.add_argument("--load", action="store_true", help="Load knowledge base")
    parser.add_argument("--processed-dir", type=str, default="./data/processed", 
                       help="Directory with processed text files")
    args = parser.parse_args()
    
    print("=" * 60)
    print("MoneyMentor - RAG Pipeline")
    print("=" * 60)
    print()
    
    # Load knowledge base if requested or no args provided
    if args.load or (not args.query):
        print("Loading knowledge base...")
        result = load_knowledge(processed_dir=args.processed_dir)
        
        if result["success"]:
            print(f"\n✅ Knowledge base loaded successfully!")
            print(f"   Documents: {result['documents_processed']}")
            print(f"   Chunks: {result['chunks_created']}")
            print(f"   Vectors: {result['vectors_indexed']}")
        else:
            print(f"\n❌ Failed to load knowledge base")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            sys.exit(1)
        
        print()
    
    # Test query if provided
    if args.query:
        print(f"Testing query: '{args.query}'")
        print("-" * 60)
        
        answer = get_finance_answer(args.query, k=5)
        
        print(f"\n📝 Answer:")
        print(answer['answer'])
        
        print(f"\n📚 Sources ({len(answer['sources'])} found):")
        for i, source in enumerate(answer['sources'], 1):
            print(f"   {i}. {source['source']} (score: {source['score']:.3f})")
            print(f"      {source['text'][:100]}...")
        
        print(f"\n🤖 Model: {answer['model']}")
    
    print()
    print("=" * 60)
    print("✅ Complete!")
    print("=" * 60)

