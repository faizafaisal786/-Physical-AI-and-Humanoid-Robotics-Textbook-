"""
Vector Store Module for RAG Chatbot
Manages ChromaDB vector database with Cohere embeddings
"""
import os
import logging
from typing import List, Optional
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorStoreManager:
    """Manages ChromaDB vector store with Cohere embeddings"""

    def __init__(self, collection_name: str = "rag_chatbot", persist_directory: str = "./chroma_db"):
        """
        Initialize vector store manager

        Args:
            collection_name: Name of the ChromaDB collection
            persist_directory: Directory to persist the database
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory

        # Check for Cohere API key
        if not os.getenv("COHERE_API_KEY"):
            raise ValueError("COHERE_API_KEY not found in environment variables")

        # Initialize Cohere embeddings
        logger.info("Initializing Cohere embeddings...")
        self.embeddings = CohereEmbeddings(
            model="embed-english-v3.0"  # Efficient and cost-effective
        )

        # Initialize or load vector store
        self.vector_store: Optional[Chroma] = None
        logger.info(f"VectorStoreManager initialized with collection: {collection_name}")

    def create_vector_store(self, documents: List[Document]) -> Chroma:
        """
        Create a new vector store from documents

        Args:
            documents: List of Document objects to embed

        Returns:
            Chroma vector store instance
        """
        try:
            logger.info(f"Creating vector store with {len(documents)} documents...")

            # Create vector store
            self.vector_store = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                collection_name=self.collection_name,
                persist_directory=self.persist_directory
            )

            logger.info(f"Vector store created successfully with {len(documents)} documents")
            return self.vector_store

        except Exception as e:
            logger.error(f"Error creating vector store: {e}")
            raise

    def load_vector_store(self) -> Chroma:
        """
        Load existing vector store from disk

        Returns:
            Chroma vector store instance
        """
        try:
            logger.info(f"Loading vector store from {self.persist_directory}...")

            self.vector_store = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )

            # Check if collection has documents
            collection_size = self.vector_store._collection.count()
            logger.info(f"Vector store loaded successfully with {collection_size} documents")

            return self.vector_store

        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
            raise

    def add_documents(self, documents: List[Document]):
        """
        Add documents to existing vector store

        Args:
            documents: List of Document objects to add
        """
        try:
            if not self.vector_store:
                logger.warning("Vector store not initialized. Creating new store...")
                self.create_vector_store(documents)
                return

            logger.info(f"Adding {len(documents)} documents to vector store...")
            self.vector_store.add_documents(documents)
            logger.info("Documents added successfully")

        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise

    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """
        Search for similar documents

        Args:
            query: Search query
            k: Number of results to return

        Returns:
            List of similar Document objects
        """
        try:
            if not self.vector_store:
                logger.error("Vector store not initialized")
                return []

            logger.info(f"Searching for: '{query[:50]}...' (top {k} results)")
            results = self.vector_store.similarity_search(query, k=k)
            logger.info(f"Found {len(results)} results")

            return results

        except Exception as e:
            logger.error(f"Error during similarity search: {e}")
            return []

    def similarity_search_with_score(self, query: str, k: int = 5) -> List[tuple[Document, float]]:
        """
        Search for similar documents with relevance scores

        Args:
            query: Search query
            k: Number of results to return

        Returns:
            List of tuples (Document, score)
        """
        try:
            if not self.vector_store:
                logger.error("Vector store not initialized")
                return []

            logger.info(f"Searching with scores for: '{query[:50]}...' (top {k} results)")
            results = self.vector_store.similarity_search_with_score(query, k=k)
            logger.info(f"Found {len(results)} results")

            return results

        except Exception as e:
            logger.error(f"Error during similarity search with score: {e}")
            return []

    def delete_collection(self):
        """Delete the entire collection"""
        try:
            if self.vector_store:
                logger.warning(f"Deleting collection: {self.collection_name}")
                self.vector_store.delete_collection()
                self.vector_store = None
                logger.info("Collection deleted successfully")

        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            raise

    def get_collection_info(self) -> dict:
        """
        Get information about the collection

        Returns:
            Dictionary with collection information
        """
        try:
            if not self.vector_store:
                return {"status": "not_initialized"}

            count = self.vector_store._collection.count()

            return {
                "status": "active",
                "collection_name": self.collection_name,
                "document_count": count,
                "persist_directory": self.persist_directory
            }

        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {"status": "error", "error": str(e)}


def main():
    """Test vector store functionality"""
    from ingest_documents import DocumentIngestion

    # Initialize components
    ingestion = DocumentIngestion(source_directory="../docusaurus_textbook/docs")
    vector_manager = VectorStoreManager()

    # Process documents
    print("Processing documents...")
    chunks, stats = ingestion.process_documents()

    if not chunks:
        print("No documents found!")
        return

    # Create vector store
    print(f"\nCreating vector store with {len(chunks)} chunks...")
    vector_manager.create_vector_store(chunks)

    # Get collection info
    info = vector_manager.get_collection_info()
    print("\n" + "="*50)
    print("Vector Store Information")
    print("="*50)
    for key, value in info.items():
        print(f"{key}: {value}")

    # Test search
    print("\n" + "="*50)
    print("Testing Search")
    print("="*50)
    test_query = "What is ROS2?"
    print(f"\nQuery: {test_query}")

    results = vector_manager.similarity_search_with_score(test_query, k=3)

    for i, (doc, score) in enumerate(results, 1):
        print(f"\nResult {i} (Score: {score:.4f}):")
        print(f"Content: {doc.page_content[:150]}...")
        print(f"Source: {doc.metadata.get('source', 'unknown')}")

    print("="*50)


if __name__ == "__main__":
    main()