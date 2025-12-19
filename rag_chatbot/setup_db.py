"""
Setup Script for RAG Chatbot Database
Ingests documents and creates ChromaDB vector store
"""
import os
import sys
from dotenv import load_dotenv
from ingest_documents import DocumentIngestion
from vector_store import VectorStoreManager

load_dotenv()


def check_api_key():
    """Check if Cohere API key is set"""
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key or api_key == "your_cohere_api_key_here":
        print("\n[X] Error: COHERE_API_KEY not set!")
        print("\nPlease follow these steps:")
        print("1. Copy .env.example to .env")
        print("2. Edit .env and add your Cohere API key")
        print("3. Get your API key from: https://dashboard.cohere.com/api-keys")
        return False
    return True


def setup_database(docs_directory="./docs", force_rebuild=False):
    """
    Set up the vector database

    Args:
        docs_directory: Path to documents directory
        force_rebuild: If True, rebuild database even if it exists
    """
    print("\n" + "="*70)
    print("RAG Chatbot - Database Setup")
    print("="*70)

    # Check API key
    if not check_api_key():
        return False

    # Check if database already exists
    db_path = "./chroma_db"
    if os.path.exists(db_path) and not force_rebuild:
        print(f"\n[!] Database already exists at: {db_path}")
        response = input("Do you want to rebuild it? (y/n): ").lower()
        if response != 'y':
            print("Setup cancelled.")
            return False

    # Initialize components
    print("\n[1] Initializing document ingestion...")
    try:
        ingestion = DocumentIngestion(source_directory=docs_directory)
    except Exception as e:
        print(f"[X] Error initializing document ingestion: {e}")
        return False

    # Process documents
    print("\n[2] Processing documents...")
    try:
        chunks, stats = ingestion.process_documents()

        if not chunks:
            print(f"[X] No documents found in {docs_directory}")
            print("\nPlease ensure you have markdown or text files in the directory.")
            return False

        print(f"\n[v] Document processing complete!")
        print(f"   - Total documents: {stats['total_documents']}")
        print(f"   - Total chunks: {stats['total_chunks']}")
        print(f"   - Total characters: {stats['total_characters']:,}")
        print(f"   - Unique sources: {stats['unique_sources']}")

    except Exception as e:
        print(f"[X] Error processing documents: {e}")
        return False

    # Initialize vector store manager
    print("\n[3] Initializing vector store...")
    try:
        vector_manager = VectorStoreManager()
    except Exception as e:
        print(f"[X] Error initializing vector store: {e}")
        return False

    # Delete existing collection if rebuilding
    if force_rebuild and os.path.exists(db_path):
        print("\n[DELETE] Deleting existing database...")
        try:
            vector_manager.load_vector_store()
            vector_manager.delete_collection()
        except Exception as e:
            print(f"[!] Warning: Could not delete existing collection: {e}")

    # Create vector store
    print("\n[4] Creating vector store (this may take a few minutes)...")
    print("   [WAIT] Generating embeddings with Cohere...")
    try:
        vector_manager.create_vector_store(chunks)
        print(f"[v] Vector store created successfully!")

    except Exception as e:
        print(f"[X] Error creating vector store: {e}")
        print("\nPossible issues:")
        print("- Invalid Cohere API key")
        print("- Insufficient Cohere credits")
        print("- Network connectivity problems")
        return False

    # Verify setup
    print("\n[5] Verifying setup...")
    try:
        info = vector_manager.get_collection_info()
        print(f"[v] Verification complete!")
        print(f"   - Collection: {info['collection_name']}")
        print(f"   - Documents: {info['document_count']}")
        print(f"   - Location: {info['persist_directory']}")

    except Exception as e:
        print(f"[!] Warning: Verification failed: {e}")

    # Test search
    print("\n[6] Testing search functionality...")
    try:
        test_query = "What is ROS2?"
        results = vector_manager.similarity_search_with_score(test_query, k=1)

        if results:
            doc, score = results[0]
            print(f"[v] Search test successful!")
            print(f"   - Query: '{test_query}'")
            print(f"   - Best match score: {score:.4f}")
            print(f"   - Preview: {doc.page_content[:100]}...")
        else:
            print(f"[!] No results found for test query")

    except Exception as e:
        print(f"[!] Search test failed: {e}")

    # Success message
    print("\n" + "="*70)
    print("[*] Database setup complete!")
    print("="*70)
    print("\n[>] You can now run the chatbot with:")
    print("   streamlit run app.py")
    print("\n" + "="*70)

    return True


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description="Setup RAG Chatbot Database")
    parser.add_argument(
        "--docs-dir",
        default="./docs",
        help="Directory containing documents (default: ./docs)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force rebuild even if database exists"
    )

    args = parser.parse_args()

    # Run setup
    success = setup_database(
        docs_directory=args.docs_dir,
        force_rebuild=args.force
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
