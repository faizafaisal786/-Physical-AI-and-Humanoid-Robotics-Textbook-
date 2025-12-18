"""
RAG Pipeline Module
Combines retrieval and generation for question answering
"""
import os
import logging
from typing import List, Dict, Optional
from dotenv import load_dotenv
from langchain_cohere import ChatCohere
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from .utils import VectorStoreManager

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGPipeline:
    """RAG Pipeline for question answering using Cohere and ChromaDB"""

    def __init__(
        self,
        model_name: str = "command-r-plus-08-2024",
        temperature: float = 0.7,
        max_tokens: int = 500,
        retrieval_k: int = 5
    ):
        """
        Initialize RAG pipeline

        Args:
            model_name: Cohere model to use (command-r-plus-08-2024, command-r-08-2024, command-a-03-2025, etc.)
            temperature: Sampling temperature for generation
            max_tokens: Maximum tokens in response
            retrieval_k: Number of documents to retrieve
        """
        # Check for Cohere API key
        if not os.getenv("COHERE_API_KEY"):
            raise ValueError("COHERE_API_KEY not found in environment variables")

        # Initialize LLM
        logger.info(f"Initializing Cohere model: {model_name}")
        self.llm = ChatCohere(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )

        # Initialize vector store manager
        self.vector_manager = VectorStoreManager()
        self.retrieval_k = retrieval_k

        # Load vector store
        try:
            self.vector_manager.load_vector_store()
            logger.info("Vector store loaded successfully")
        except Exception as e:
            logger.warning(f"Could not load vector store: {e}")
            logger.info("You need to create a vector store first by running: python setup_db.py")

        # Custom prompt template
        self.prompt_template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer based on the context, just say that you don't know, don't try to make up an answer.
Always cite the source documents when possible.

Context:
{context}

Question: {question}

Answer: """

        self.prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=["context", "question"]
        )

        logger.info("RAG Pipeline initialized successfully")

    def query(self, question: str) -> Dict:
        """
        Process a question through the RAG pipeline

        Args:
            question: User's question

        Returns:
            Dictionary with answer and metadata
        """
        try:
            if not self.vector_manager.vector_store:
                return {
                    "question": question,
                    "answer": "Vector store not initialized. Please run setup_db.py first.",
                    "source_documents": [],
                    "error": "Vector store not available"
                }

            logger.info(f"Processing question: '{question[:50]}...'")

            # Retrieve relevant documents
            docs_with_scores = self.vector_manager.similarity_search_with_score(
                question,
                k=self.retrieval_k
            )

            if not docs_with_scores:
                return {
                    "question": question,
                    "answer": "I couldn't find any relevant information to answer your question.",
                    "source_documents": [],
                    "error": "No relevant documents found"
                }

            # Extract documents and scores
            docs = [doc for doc, score in docs_with_scores]
            scores = [score for doc, score in docs_with_scores]

            # Create context from retrieved documents
            context = "\n\n".join([
                f"Document {i+1} (Relevance: {scores[i]:.4f}):\n{doc.page_content}"
                for i, doc in enumerate(docs)
            ])

            # Generate answer using LLM with the prompt
            formatted_prompt = self.prompt.format(context=context, question=question)
            response = self.llm.invoke(formatted_prompt)
            answer = response.content

            # Prepare source documents info
            sources = []
            for i, (doc, score) in enumerate(docs_with_scores):
                sources.append({
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    "source": doc.metadata.get('source', 'unknown'),
                    "relevance_score": float(score)
                })

            logger.info(f"Generated answer with {len(sources)} source documents")

            return {
                "question": question,
                "answer": answer,
                "source_documents": sources,
                "num_sources": len(sources)
            }

        except Exception as e:
            logger.error(f"Error processing question: {e}")
            return {
                "question": question,
                "answer": "Sorry, I encountered an error while processing your question.",
                "source_documents": [],
                "error": str(e)
            }

    def chat(self, question: str) -> str:
        """
        Simple chat interface that returns just the answer

        Args:
            question: User's question

        Returns:
            Answer string
        """
        result = self.query(question)
        return result.get("answer", "I couldn't generate an answer.")

    def get_context(self, question: str, k: int = None) -> List[Dict]:
        """
        Retrieve relevant context without generating an answer

        Args:
            question: Query to search for
            k: Number of documents to retrieve (uses default if not specified)

        Returns:
            List of relevant documents with scores
        """
        k = k or self.retrieval_k

        try:
            if not self.vector_manager.vector_store:
                logger.error("Vector store not initialized")
                return []

            docs_with_scores = self.vector_manager.similarity_search_with_score(
                question,
                k=k
            )

            context = []
            for doc, score in docs_with_scores:
                context.append({
                    "content": doc.page_content,
                    "source": doc.metadata.get('source', 'unknown'),
                    "relevance_score": float(score)
                })

            return context

        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return []


def ask_question(question: str) -> str:
    """
    Simple function to ask a question and get an answer
    Uses the RAG pipeline for question answering
    """
    try:
        # Initialize pipeline with default settings
        pipeline = RAGPipeline()
        return pipeline.chat(question)
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    """Test RAG pipeline"""
    # Initialize pipeline
    print("Initializing RAG Pipeline...")
    pipeline = RAGPipeline(
        model_name="command-r-plus-08-2024",
        temperature=0.7,
        retrieval_k=3
    )

    # Test questions
    test_questions = [
        "What is ROS2?",
        "Explain humanoid robotics",
        "What are Vision-Language-Action models?",
        "How does simulation work in robotics?"
    ]

    print("\n" + "="*70)
    print("RAG Pipeline Test")
    print("="*70)

    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*70}")
        print(f"Question {i}: {question}")
        print('-'*70)

        result = pipeline.query(question)

        print(f"\nAnswer:\n{result['answer']}")

        if result.get('source_documents'):
            print(f"\nSources ({result['num_sources']}):")
            for j, source in enumerate(result['source_documents'], 1):
                print(f"\n  {j}. {source['source']}")
                print(f"     Relevance: {source['relevance_score']:.4f}")
                print(f"     Content: {source['content'][:100]}...")

        if result.get('error'):
            print(f"\nError: {result['error']}")

    print("\n" + "="*70)


if __name__ == "__main__":
    main()
    """Test RAG pipeline"""
    # Initialize pipeline
    print("Initializing RAG Pipeline...")
    pipeline = RAGPipeline(
        model_name="command-r-plus-08-2024",
        temperature=0.7,
        retrieval_k=3
    )

    # Test questions
    test_questions = [
        "What is ROS2?",
        "Explain humanoid robotics",
        "What are Vision-Language-Action models?",
        "How does simulation work in robotics?"
    ]

    print("\n" + "="*70)
    print("RAG Pipeline Test")
    print("="*70)

    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*70}")
        print(f"Question {i}: {question}")
        print('-'*70)

        result = pipeline.query(question)

        print(f"\nAnswer:\n{result['answer']}")

        if result.get('source_documents'):
            print(f"\nSources ({result['num_sources']}):")
            for j, source in enumerate(result['source_documents'], 1):
                print(f"\n  {j}. {source['source']}")
                print(f"     Relevance: {source['relevance_score']:.4f}")
                print(f"     Content: {source['content'][:100]}...")

        if result.get('error'):
            print(f"\nError: {result['error']}")

    print("\n" + "="*70)


if __name__ == "__main__":
    main()