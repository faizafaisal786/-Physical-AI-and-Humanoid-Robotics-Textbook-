"""
Quick script to create vector database for RAG chatbot
"""
import os
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

def create_vector_db():
    print("="*70)
    print("Creating Vector Database for RAG Chatbot")
    print("="*70)

    # Check for documents
    docs_path = "docusaurus_textbook/docs"
    if not os.path.exists(docs_path):
        print(f"\n[ERROR] Documents directory not found at {docs_path}")
        return False

    print(f"\n[*] Loading documents from: {docs_path}")

    # Load markdown documents
    loader = DirectoryLoader(
        docs_path,
        glob="**/*.md",
        loader_cls=TextLoader,
        show_progress=True,
        use_multithreading=True
    )

    documents = loader.load()
    print(f"[+] Loaded {len(documents)} documents")

    # Split documents into chunks
    print("\n[*] Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    chunks = text_splitter.split_documents(documents)
    print(f"[+] Created {len(chunks)} chunks")

    # Create embeddings
    print("\n[*] Initializing Cohere embeddings...")
    embeddings = CohereEmbeddings(model="embed-english-v3.0")

    # Create vector store
    print("\n[*] Creating ChromaDB vector store...")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name="rag_chatbot",
        persist_directory="./chroma_db"
    )

    print(f"[+] Vector store created with {len(chunks)} chunks")
    print(f"[+] Location: ./chroma_db")

    # Test search
    print("\n[*] Testing vector store with a sample query...")
    test_query = "What is ROS2?"
    results = vector_store.similarity_search(test_query, k=3)
    print(f"[+] Found {len(results)} relevant documents")
    print(f"    Sample result: {results[0].page_content[:100]}...")

    print("\n" + "="*70)
    print("[SUCCESS] Vector Database Created Successfully!")
    print("="*70)
    return True

if __name__ == "__main__":
    success = create_vector_db()
    if success:
        print("\n[*] You can now run the Streamlit app with: streamlit run streamlit_app.py")
    else:
        print("\n[ERROR] Failed to create vector database")
