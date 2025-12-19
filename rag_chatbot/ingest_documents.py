"""
Document Ingestion Module for RAG Chatbot
Reads and processes local Text/Markdown files for embedding
"""
import os
import logging
from pathlib import Path
from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentIngestion:
    """Handles ingestion of text and markdown documents"""

    def __init__(self, source_directory: str = "../docs", chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize document ingestion

        Args:
            source_directory: Path to directory containing documents
            chunk_size: Size of text chunks for processing
            chunk_overlap: Overlap between chunks to preserve context
        """
        self.source_directory = source_directory
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

        logger.info(f"Initialized DocumentIngestion for directory: {source_directory}")

    def load_documents(self) -> List[Document]:
        """
        Load all text and markdown documents from source directory

        Returns:
            List of Document objects
        """
        documents = []

        try:
            # Check if directory exists
            if not os.path.exists(self.source_directory):
                logger.warning(f"Directory not found: {self.source_directory}")
                return documents

            # Load markdown files
            logger.info("Loading markdown files...")
            md_loader = DirectoryLoader(
                self.source_directory,
                glob="**/*.md",
                loader_cls=TextLoader,
                loader_kwargs={'encoding': 'utf-8'},
                recursive=True,
                show_progress=True
            )
            md_docs = md_loader.load()
            documents.extend(md_docs)
            logger.info(f"Loaded {len(md_docs)} markdown files")

            # Load text files
            logger.info("Loading text files...")
            txt_loader = DirectoryLoader(
                self.source_directory,
                glob="**/*.txt",
                loader_cls=TextLoader,
                loader_kwargs={'encoding': 'utf-8'},
                recursive=True,
                show_progress=True
            )
            txt_docs = txt_loader.load()
            documents.extend(txt_docs)
            logger.info(f"Loaded {len(txt_docs)} text files")

            logger.info(f"Total documents loaded: {len(documents)}")

        except Exception as e:
            logger.error(f"Error loading documents: {e}")
            raise

        return documents

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks

        Args:
            documents: List of Document objects

        Returns:
            List of chunked Document objects
        """
        try:
            logger.info("Splitting documents into chunks...")
            chunks = self.text_splitter.split_documents(documents)
            logger.info(f"Created {len(chunks)} chunks from {len(documents)} documents")
            return chunks

        except Exception as e:
            logger.error(f"Error splitting documents: {e}")
            raise

    def get_document_stats(self, documents: List[Document]) -> Dict:
        """
        Get statistics about loaded documents

        Args:
            documents: List of Document objects

        Returns:
            Dictionary with statistics
        """
        total_chars = sum(len(doc.page_content) for doc in documents)
        sources = set(doc.metadata.get('source', 'unknown') for doc in documents)

        stats = {
            'total_documents': len(documents),
            'total_characters': total_chars,
            'avg_chars_per_doc': total_chars // len(documents) if documents else 0,
            'unique_sources': len(sources)
        }

        return stats

    def process_documents(self) -> tuple[List[Document], Dict]:
        """
        Complete document processing pipeline

        Returns:
            Tuple of (chunked documents, statistics)
        """
        # Load documents
        documents = self.load_documents()

        if not documents:
            logger.warning("No documents found to process")
            return [], {}

        # Get stats before chunking
        stats = self.get_document_stats(documents)
        logger.info(f"Document stats: {stats}")

        # Split into chunks
        chunks = self.split_documents(documents)
        stats['total_chunks'] = len(chunks)

        return chunks, stats


def main():
    """Test document ingestion"""
    # Initialize ingestion
    ingestion = DocumentIngestion(source_directory="../docusaurus_textbook/docs")

    # Process documents
    chunks, stats = ingestion.process_documents()

    # Display results
    print("\n" + "="*50)
    print("Document Ingestion Results")
    print("="*50)
    print(f"Total documents: {stats.get('total_documents', 0)}")
    print(f"Total chunks: {stats.get('total_chunks', 0)}")
    print(f"Total characters: {stats.get('total_characters', 0):,}")
    print(f"Average chars per document: {stats.get('avg_chars_per_doc', 0):,}")
    print(f"Unique sources: {stats.get('unique_sources', 0)}")

    # Show sample chunks
    if chunks:
        print("\nSample chunk:")
        print("-"*50)
        print(f"Content: {chunks[0].page_content[:200]}...")
        print(f"Source: {chunks[0].metadata.get('source', 'unknown')}")

    print("="*50)


if __name__ == "__main__":
    main()
