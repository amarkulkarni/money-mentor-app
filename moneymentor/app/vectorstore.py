"""
MoneyMentor - Vector Store Management
Handles vector database operations with Qdrant
"""
import os
import logging
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from qdrant_client.http import exceptions as qdrant_exceptions

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global client instance (singleton pattern)
_client_instance: Optional[QdrantClient] = None


def get_qdrant_client() -> Optional[QdrantClient]:
    """
    Get or create a Qdrant client connection.
    
    Reads QDRANT_URL from environment variable, defaults to http://localhost:6333.
    Supports both local and cloud deployments with optional API key.
    Uses singleton pattern to reuse connection.
    
    Returns:
        QdrantClient instance if connection successful, None otherwise
        
    Environment Variables:
        QDRANT_URL: URL of Qdrant instance (default: http://localhost:6333)
        QDRANT_API_KEY: API key for Qdrant Cloud (optional, for cloud deployments)
    """
    global _client_instance
    
    if _client_instance is not None:
        return _client_instance
    
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    
    try:
        logger.info(f"🔌 Connecting to Qdrant at {qdrant_url}...")
        
        # Create client with or without API key
        if qdrant_api_key:
            logger.info("   Using API key authentication (Qdrant Cloud)")
            client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        else:
            client = QdrantClient(url=qdrant_url)
        
        # Test connection by fetching collections
        client.get_collections()
        
        logger.info("✅ Successfully connected to Qdrant")
        _client_instance = client
        return client
        
    except qdrant_exceptions.UnexpectedResponse as e:
        logger.error(f"❌ Failed to connect to Qdrant at {qdrant_url}")
        logger.error(f"   Error: {e}")
        logger.error(f"   💡 Make sure Qdrant is running:")
        logger.error(f"      Local: ./qdrant  or  docker run -p 6333:6333 qdrant/qdrant")
        logger.error(f"      Cloud: Check QDRANT_URL and QDRANT_API_KEY are set correctly")
        return None
        
    except Exception as e:
        logger.error(f"❌ Unexpected error connecting to Qdrant: {e}")
        logger.error(f"   💡 Check if Qdrant is running at {qdrant_url}")
        return None


def ensure_collection(
    collection_name: str,
    vector_size: int,
    distance: Distance = Distance.COSINE
) -> bool:
    """
    Ensure a collection exists in Qdrant, creating it if necessary.
    
    Args:
        collection_name: Name of the collection
        vector_size: Dimension of the vectors (e.g., 1536 for OpenAI embeddings)
        distance: Distance metric to use (COSINE, EUCLID, or DOT)
        
    Returns:
        True if collection exists or was created successfully, False otherwise
        
    Example:
        >>> ensure_collection("moneymentor", vector_size=1536)
        True
    """
    client = get_qdrant_client()
    if client is None:
        logger.error("❌ Cannot ensure collection: Qdrant client not available")
        return False
    
    try:
        # Check if collection exists
        collections = client.get_collections().collections
        collection_names = [col.name for col in collections]
        
        if collection_name in collection_names:
            logger.info(f"✅ Collection '{collection_name}' already exists")
            return True
        
        # Create collection if it doesn't exist
        logger.info(f"📦 Creating collection '{collection_name}' with vector size {vector_size}...")
        
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=distance
            )
        )
        
        logger.info(f"✅ Collection '{collection_name}' created successfully")
        return True
        
    except qdrant_exceptions.UnexpectedResponse as e:
        logger.error(f"❌ Failed to create collection '{collection_name}': {e}")
        return False
        
    except Exception as e:
        logger.error(f"❌ Unexpected error ensuring collection: {e}")
        return False


def upsert_points(
    collection_name: str,
    points: List[PointStruct]
) -> bool:
    """
    Upsert (insert or update) points into a Qdrant collection.
    
    Args:
        collection_name: Name of the collection
        points: List of PointStruct objects to upsert
                Each point should have: id, vector, and optional payload
        
    Returns:
        True if upsert successful, False otherwise
        
    Example:
        >>> from qdrant_client.models import PointStruct
        >>> points = [
        ...     PointStruct(
        ...         id=1,
        ...         vector=[0.1, 0.2, 0.3, ...],  # embedding vector
        ...         payload={"text": "Sample text", "source": "doc1.pdf"}
        ...     )
        ... ]
        >>> upsert_points("moneymentor", points)
        True
    """
    client = get_qdrant_client()
    if client is None:
        logger.error("❌ Cannot upsert points: Qdrant client not available")
        return False
    
    if not points:
        logger.warning("⚠️  No points to upsert")
        return True
    
    try:
        logger.info(f"💾 Upserting {len(points)} point(s) to '{collection_name}'...")
        
        client.upsert(
            collection_name=collection_name,
            points=points
        )
        
        logger.info(f"✅ Successfully upserted {len(points)} point(s)")
        return True
        
    except qdrant_exceptions.UnexpectedResponse as e:
        logger.error(f"❌ Failed to upsert points to '{collection_name}': {e}")
        logger.error(f"   💡 Make sure the collection exists and vector dimensions match")
        return False
        
    except Exception as e:
        logger.error(f"❌ Unexpected error upserting points: {e}")
        return False


def search_points(
    collection_name: str,
    query_vector: List[float],
    top_k: int = 5,
    score_threshold: Optional[float] = None
) -> Optional[List[Dict[str, Any]]]:
    """
    Search for similar vectors in a collection.
    
    Args:
        collection_name: Name of the collection to search
        query_vector: Query embedding vector
        top_k: Number of results to return
        score_threshold: Minimum similarity score (optional)
        
    Returns:
        List of search results with scores and payloads, or None if error
        
    Example:
        >>> results = search_points("moneymentor", query_vector=[0.1, 0.2, ...], top_k=5)
        >>> for result in results:
        ...     print(f"Score: {result['score']}, Text: {result['payload']['text']}")
    """
    client = get_qdrant_client()
    if client is None:
        logger.error("❌ Cannot search: Qdrant client not available")
        return None
    
    try:
        search_result = client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=top_k,
            score_threshold=score_threshold
        )
        
        # Convert to more usable format
        results = [
            {
                "id": hit.id,
                "score": hit.score,
                "payload": hit.payload
            }
            for hit in search_result
        ]
        
        logger.info(f"🔍 Found {len(results)} result(s) in '{collection_name}'")
        return results
        
    except qdrant_exceptions.UnexpectedResponse as e:
        logger.error(f"❌ Failed to search in '{collection_name}': {e}")
        return None
        
    except Exception as e:
        logger.error(f"❌ Unexpected error during search: {e}")
        return None


def get_collection_info(collection_name: str) -> Optional[Dict[str, Any]]:
    """
    Get information about a collection.
    
    Args:
        collection_name: Name of the collection
        
    Returns:
        Dictionary with collection info, or None if error
    """
    client = get_qdrant_client()
    if client is None:
        return None
    
    try:
        info = client.get_collection(collection_name)
        return {
            "name": collection_name,
            "vector_size": info.config.params.vectors.size,
            "distance": info.config.params.vectors.distance,
            "points_count": info.points_count
        }
    except Exception as e:
        logger.error(f"❌ Failed to get collection info: {e}")
        return None


# Legacy VectorStore class for backward compatibility
class VectorStore:
    """
    Vector store interface for managing embeddings and similarity search.
    This class wraps the functional API above.
    """
    
    def __init__(self, collection_name: str = "moneymentor"):
        """
        Initialize vector store connection
        
        Args:
            collection_name: Name of the collection in Qdrant
        """
        self.collection_name = collection_name
        self.client = get_qdrant_client()
    
    def ensure_collection(self, vector_size: int) -> bool:
        """Ensure the collection exists"""
        return ensure_collection(self.collection_name, vector_size)
    
    def upsert_points(self, points: List[PointStruct]) -> bool:
        """Upsert points to the collection"""
        return upsert_points(self.collection_name, points)
    
    def search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        score_threshold: Optional[float] = None
    ) -> Optional[List[Dict[str, Any]]]:
        """Search for similar vectors"""
        return search_points(self.collection_name, query_vector, top_k, score_threshold)
    
    def get_info(self) -> Optional[Dict[str, Any]]:
        """Get collection information"""
        return get_collection_info(self.collection_name)


if __name__ == "__main__":
    """
    Demo script to test Qdrant connection and basic operations
    Run: python vectorstore.py
    """
    print("=" * 60)
    print("MoneyMentor - Vector Store Test")
    print("=" * 60)
    print()
    
    # Test connection
    print("Testing Qdrant connection...")
    client = get_qdrant_client()
    
    if client is None:
        print("\n❌ Cannot proceed without Qdrant connection")
        print("💡 Start Qdrant with: docker run -p 6333:6333 qdrant/qdrant")
        exit(1)
    
    print()
    
    # Test collection creation
    print("Testing collection creation...")
    collection_name = "test_collection"
    vector_size = 1536  # OpenAI embedding size
    
    success = ensure_collection(collection_name, vector_size)
    
    if success:
        print()
        # Get collection info
        print("Getting collection info...")
        info = get_collection_info(collection_name)
        if info:
            print(f"   Collection: {info['name']}")
            print(f"   Vector size: {info['vector_size']}")
            print(f"   Distance: {info['distance']}")
            print(f"   Points: {info['points_count']}")
    
    print()
    print("=" * 60)
    print("✅ Vector store test complete!")
    print("=" * 60)

