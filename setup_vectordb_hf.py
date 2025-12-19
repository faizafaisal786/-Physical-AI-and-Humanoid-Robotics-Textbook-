"""
Setup script to create vector database on HF Spaces startup
This runs automatically when the Space builds
"""
import os
import sys
from pathlib import Path

def setup_vector_db():
    """Create vector database if it doesn't exist"""
    db_path = Path("./chroma_db")

    # Check if database already exists
    if db_path.exists() and (db_path / "chroma.sqlite3").exists():
        print("[*] Vector database already exists, skipping creation")
        return True

    print("[*] Creating vector database...")

    try:
        from langchain_community.document_loaders import DirectoryLoader, TextLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_cohere import CohereEmbeddings
        from langchain_community.vectorstores import Chroma

        docs_path = "docusaurus_textbook/docs"

        if not os.path.exists(docs_path):
            print(f"[ERROR] Documents directory not found at {docs_path}")
            return False

        print(f"[*] Loading documents from: {docs_path}")

        # Load markdown documents
        loader = DirectoryLoader(
            docs_path,
            glob="**/*.md",
            loader_cls=TextLoader,
            show_progress=False,
            use_multithreading=True
        )

        documents = loader.load()
        print(f"[+] Loaded {len(documents)} documents")

        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

        chunks = text_splitter.split_documents(documents)
        print(f"[+] Created {len(chunks)} chunks")

        # Create embeddings
        print("[*] Initializing Cohere embeddings...")
        embeddings = CohereEmbeddings(model="embed-english-v3.0")

        # Create vector store
        print("[*] Creating ChromaDB vector store...")
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name="rag_chatbot",
            persist_directory="./chroma_db"
        )

        print(f"[SUCCESS] Vector database created with {len(chunks)} chunks")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to create vector database: {e}")
        return False

if __name__ == "__main__":
    success = setup_vector_db()
    sys.exit(0 if success else 1)
