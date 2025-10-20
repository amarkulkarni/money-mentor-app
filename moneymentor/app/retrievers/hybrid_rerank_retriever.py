"""
MoneyMentor - Hybrid Retriever with Reranking

Combines BM25 (keyword-based) and Vector (semantic) search, 
then reranks results using Cohere for optimal precision.

Architecture:
1. BM25 Retriever: Captures exact keyword matches (e.g., "401k", "Roth IRA")
2. Vector Retriever: Captures semantic similarity
3. Ensemble: Combines both with weighted fusion (40% BM25, 60% Vector)
4. Cohere Reranker: Cross-encoder reranks top-20 results to get best top-5
"""

import os
import logging
from typing import List, Optional
from pathlib import Path

from langchain.schema import Document
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
import cohere

# Import from parent modules
import sys
sys.path.append(str(Path(__file__).parent.parent))
from vectorstore import get_qdrant_client

logger = logging.getLogger(__name__)

# Constants
COLLECTION_NAME = "moneymentor_knowledge"
EMBEDDING_MODEL = "text-embedding-3-small"
BM25_WEIGHT = 0.4  # 40% weight for keyword matching
VECTOR_WEIGHT = 0.6  # 60% weight for semantic similarity
INITIAL_K = 20  # Retrieve more docs for reranking
FINAL_K = 5  # Return top 5 after reranking


def load_documents_for_bm25(processed_dir: str = "./data/processed") -> List[Document]:
    """
    Load all processed documents for BM25 indexing.
    
    Args:
        processed_dir: Directory containing processed text files
        
    Returns:
        List of Document objects with text and metadata
    """
    logger.info(f"📂 Loading documents from {processed_dir} for BM25 indexing...")
    
    processed_path = Path(processed_dir)
    if not processed_path.exists():
        logger.error(f"❌ Processed directory not found: {processed_dir}")
        return []
    
    documents = []
    txt_files = list(processed_path.glob("*.txt"))
    
    for file_path in txt_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            if text.strip():
                doc = Document(
                    page_content=text,
                    metadata={
                        "source": file_path.name,
                        "file_path": str(file_path)
                    }
                )
                documents.append(doc)
                logger.info(f"   ✓ Loaded {file_path.name} ({len(text)} chars)")
        except Exception as e:
            logger.error(f"   ❌ Error loading {file_path.name}: {e}")
    
    logger.info(f"✅ Loaded {len(documents)} documents for BM25")
    return documents


def build_hybrid_rerank_retriever(
    collection_name: str = COLLECTION_NAME,
    processed_dir: str = "./data/processed",
    k: int = FINAL_K
) -> "HybridReranker":
    """
    Build a hybrid retriever with BM25 + Vector search and Cohere reranking.
    
    This creates a multi-stage retrieval pipeline:
    1. BM25 retrieves top-20 by keyword relevance
    2. Vector retrieves top-20 by semantic similarity  
    3. Ensemble combines both (40% BM25, 60% Vector) → top-20 diverse docs
    4. Cohere reranks top-20 → return top-k best matches
    
    Args:
        collection_name: Qdrant collection name
        processed_dir: Directory with processed documents
        k: Final number of documents to return (after reranking)
        
    Returns:
        HybridReranker instance configured and ready to use
    """
    logger.info("=" * 70)
    logger.info("🚀 Building Hybrid Retriever with Reranking")
    logger.info("=" * 70)
    
    # Check API keys
    api_key = os.getenv("OPENAI_API_KEY")
    cohere_key = os.getenv("COHERE_API_KEY")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment")
    if not cohere_key:
        raise ValueError("COHERE_API_KEY not found in environment")
    
    # Step 1: Build BM25 Retriever (keyword-based)
    logger.info("\n📚 Step 1: Building BM25 Retriever (keyword search)...")
    documents = load_documents_for_bm25(processed_dir)
    
    if not documents:
        raise ValueError(f"No documents found in {processed_dir}")
    
    bm25_retriever = BM25Retriever.from_documents(documents)
    bm25_retriever.k = INITIAL_K
    logger.info(f"   ✓ BM25 configured to retrieve top-{INITIAL_K} by keyword relevance")
    
    # Step 2: Build Vector Retriever (semantic)
    logger.info("\n🔍 Step 2: Building Vector Retriever (semantic search)...")
    client = get_qdrant_client()
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=api_key)
    
    vectorstore = Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embeddings,
        content_payload_key="text"
    )
    
    vector_retriever = vectorstore.as_retriever(search_kwargs={"k": INITIAL_K})
    logger.info(f"   ✓ Vector retriever configured to retrieve top-{INITIAL_K} by cosine similarity")
    
    # Step 3: Create Ensemble (Hybrid) Retriever
    logger.info("\n🔄 Step 3: Creating Ensemble Retriever (hybrid)...")
    hybrid_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vector_retriever],
        weights=[BM25_WEIGHT, VECTOR_WEIGHT]
    )
    logger.info(f"   ✓ Ensemble: {int(BM25_WEIGHT*100)}% BM25 + {int(VECTOR_WEIGHT*100)}% Vector")
    logger.info(f"   ✓ Will retrieve ~{INITIAL_K} diverse documents")
    
    # Step 4: Initialize Cohere Reranker
    logger.info("\n🎯 Step 4: Initializing Cohere Reranker...")
    cohere_client = cohere.Client(cohere_key)
    logger.info(f"   ✓ Cohere client initialized (model: rerank-english-v2.0)")
    logger.info(f"   ✓ Will rerank to return top-{k} documents")
    
    # Create custom reranker wrapper
    reranker = HybridReranker(
        base_retriever=hybrid_retriever,
        cohere_client=cohere_client,
        top_k=k
    )
    
    logger.info("\n" + "=" * 70)
    logger.info("✅ Hybrid Rerank Retriever Ready!")
    logger.info("=" * 70)
    logger.info(f"Pipeline: BM25 + Vector → Ensemble → Cohere Rerank → Top-{k}")
    logger.info("=" * 70 + "\n")
    
    return reranker


class HybridReranker:
    """
    Custom retriever that combines hybrid search with Cohere reranking.
    
    This wraps an EnsembleRetriever and adds Cohere reranking on top.
    Compatible with LangChain's retriever interface.
    """
    
    def __init__(
        self,
        base_retriever: EnsembleRetriever,
        cohere_client: cohere.Client,
        top_k: int = 5
    ):
        """
        Initialize the hybrid reranker.
        
        Args:
            base_retriever: Ensemble retriever (BM25 + Vector)
            cohere_client: Cohere API client
            top_k: Number of final documents to return
        """
        self.base_retriever = base_retriever
        self.cohere_client = cohere_client
        self.top_k = top_k
    
    def get_relevant_documents(self, query: str) -> List[Document]:
        """
        Retrieve and rerank documents for a query.
        
        Args:
            query: User's search query
            
        Returns:
            Top-k reranked documents
        """
        logger.info(f"🔍 Hybrid Rerank: Retrieving for query: '{query[:50]}...'")
        
        # Step 1: Get initial documents from hybrid retriever
        docs = self.base_retriever.get_relevant_documents(query)
        logger.info(f"   ✓ Retrieved {len(docs)} documents from ensemble")
        
        if not docs:
            logger.warning("   ⚠️  No documents retrieved from base retriever")
            return []
        
        # Step 2: Rerank with Cohere
        try:
            # Prepare documents for Cohere
            doc_texts = [doc.page_content for doc in docs]
            
            # Call Cohere Rerank API
            rerank_response = self.cohere_client.rerank(
                query=query,
                documents=doc_texts,
                top_n=self.top_k,
                model="rerank-english-v2.0"
            )
            
            # Extract reranked documents in new order
            reranked_docs = []
            for result in rerank_response.results:
                original_doc = docs[result.index]
                
                # Add rerank score to metadata
                original_doc.metadata["rerank_score"] = result.relevance_score
                original_doc.metadata["rerank_position"] = len(reranked_docs) + 1
                
                reranked_docs.append(original_doc)
            
            logger.info(f"   ✓ Reranked to top-{len(reranked_docs)} documents")
            logger.info(f"   📊 Best score: {reranked_docs[0].metadata['rerank_score']:.3f}")
            
            return reranked_docs
            
        except Exception as e:
            logger.error(f"   ❌ Reranking failed: {e}")
            logger.warning(f"   ⚠️  Falling back to base retriever results")
            # Fallback: return original results limited to top_k
            return docs[:self.top_k]
    
    async def aget_relevant_documents(self, query: str) -> List[Document]:
        """Async version - currently just calls sync version."""
        return self.get_relevant_documents(query)


def test_retriever():
    """
    Test the hybrid rerank retriever with sample queries.
    """
    print("\n" + "=" * 70)
    print("Testing Hybrid Rerank Retriever")
    print("=" * 70 + "\n")
    
    try:
        retriever = build_hybrid_rerank_retriever(k=3)
        
        test_queries = [
            "What is compound interest?",
            "What is a 401k?",
            "How do I start building credit?"
        ]
        
        for query in test_queries:
            print(f"\n{'='*70}")
            print(f"Query: {query}")
            print('='*70)
            
            docs = retriever.get_relevant_documents(query)
            
            print(f"\n📚 Retrieved {len(docs)} documents:\n")
            for i, doc in enumerate(docs, 1):
                source = doc.metadata.get("source", "unknown")
                score = doc.metadata.get("rerank_score", 0.0)
                preview = doc.page_content[:150].replace("\n", " ")
                
                print(f"{i}. {source} (score: {score:.3f})")
                print(f"   {preview}...\n")
        
        print("\n" + "=" * 70)
        print("✅ Test Complete!")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    """
    CLI for testing the hybrid rerank retriever.
    
    Usage:
        python -m app.retrievers.hybrid_rerank_retriever
    """
    from dotenv import load_dotenv
    load_dotenv()
    
    test_retriever()

