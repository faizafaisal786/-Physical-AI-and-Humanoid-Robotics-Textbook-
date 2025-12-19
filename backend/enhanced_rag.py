"""
Enhanced RAG Pipeline Module
Combines retrieval and generation for question answering with support for both Cohere and Hugging Face models
"""
import os
import logging
from typing import List, Dict, Optional, Union
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .utils import VectorStoreManager
from .hf_utils import HFTokenManager, get_hf_embeddings

# Import appropriate LLM classes based on availability
try:
    from langchain_cohere import ChatCohere
    COHERE_AVAILABLE = True
except ImportError:
    COHERE_AVAILABLE = False
    ChatCohere = None

try:
    from langchain_huggingface import HuggingFaceEndpoint
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    HuggingFaceEndpoint = None

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnhancedRAGPipeline:
    """Enhanced RAG Pipeline supporting both Cohere and Hugging Face models"""

    def __init__(
        self,
        model_provider: str = "cohere",  # "cohere" or "huggingface"
        model_name: str = "command-r-plus-08-2024",
        temperature: float = 0.7,
        max_tokens: int = 500,
        retrieval_k: int = 5
    ):
        """
        Initialize enhanced RAG pipeline

        Args:
            model_provider: "cohere" or "huggingface"
            model_name: Model name to use
            temperature: Sampling temperature for generation
            max_tokens: Maximum tokens in response
            retrieval_k: Number of documents to retrieve
        """
        self.model_provider = model_provider
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.retrieval_k = retrieval_k

        # Initialize appropriate LLM based on provider
        if model_provider.lower() == "cohere":
            if not COHERE_AVAILABLE:
                raise ImportError("langchain-cohere is required for Cohere models")
            
            if not os.getenv("COHERE_API_KEY"):
                raise ValueError("COHERE_API_KEY not found in environment variables")
                
            logger.info(f"Initializing Cohere model: {model_name}")
            self.llm = ChatCohere(
                model=model_name,
                temperature=temperature,
                max_tokens=max_tokens
            )
        elif model_provider.lower() == "huggingface":
            if not HF_AVAILABLE:
                raise ImportError("langchain-huggingface is required for Hugging Face models")
                
            if not HFTokenManager.is_token_available():
                raise ValueError("HF_TOKEN not found in environment variables")
            
            logger.info(f"Initializing Hugging Face model: {model_name}")
            self.llm = HuggingFaceEndpoint(
                repo_id=model_name,
                huggingfacehub_api_token=HFTokenManager().get_token(),
                temperature=temperature,
                max_new_tokens=max_tokens,
                repetition_penalty=1.03,
            )
        else:
            raise ValueError(f"Unsupported model provider: {model_provider}")

        # Initialize vector store manager
        self.vector_manager = VectorStoreManager()

        # Determine embedding type based on provider
        if model_provider.lower() == "huggingface":
            # Use Hugging Face embeddings if available
            try:
                self.embeddings = get_hf_embeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2"
                )
                self.vector_manager = VectorStoreManager(embeddings=self.embeddings)
            except Exception as e:
                logger.warning(f"Could not initialize Hugging Face embeddings: {e}")
                # Fall back to Cohere if Hugging Face initialization fails
                if COHERE_AVAILABLE and os.getenv("COHERE_API_KEY"):
                    from langchain_cohere import CohereEmbeddings
                    self.embeddings = CohereEmbeddings(model="embed-english-v3.0")
                    self.vector_manager = VectorStoreManager(embeddings=self.embeddings)
                else:
                    raise ValueError("Could not initialize any embedding model")
        else:
            # Default to Cohere embeddings
            from langchain_cohere import CohereEmbeddings
            self.embeddings = CohereEmbeddings(model="embed-english-v3.0")
            self.vector_manager = VectorStoreManager(embeddings=self.embeddings)

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

        logger.info(f"Enhanced RAG Pipeline initialized successfully with {model_provider} backend")

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


def ask_question_with_provider(
    question: str, 
    model_provider: str = "cohere", 
    model_name: str = "command-r-plus-08-2024"
) -> str:
    """
    Function to ask a question using a specific model provider
    Uses the Enhanced RAG pipeline for question answering
    """
    try:
        # Initialize pipeline with specified provider
        pipeline = EnhancedRAGPipeline(
            model_provider=model_provider,
            model_name=model_name
        )
        return pipeline.chat(question)
    except Exception as e:
        return f"Error: {str(e)}"


def ask_question(question: str) -> str:
    """
    Simple function to ask a question and get an answer (defaults to Cohere)
    Uses the Enhanced RAG pipeline for question answering
    """
    try:
        # Initialize pipeline with default settings (Cohere)
        pipeline = EnhancedRAGPipeline()
        return pipeline.chat(question)
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    """Test Enhanced RAG pipeline"""
    print("Testing Enhanced RAG Pipeline with different providers...")
    
    # Test with Cohere (if available)
    if COHERE_AVAILABLE and os.getenv("COHERE_API_KEY"):
        print("\n" + "="*70)
        print("Testing with Cohere")
        print("="*70)
        
        try:
            cohere_pipeline = EnhancedRAGPipeline(
                model_provider="cohere",
                model_name="command-r-plus-08-2024",
                temperature=0.7,
                retrieval_k=3
            )
            
            question = "What is ROS2?"
            result = cohere_pipeline.query(question)
            
            print(f"Question: {question}")
            print(f"Answer: {result['answer']}")
            print(f"Sources: {result['num_sources']}")
            
        except Exception as e:
            print(f"Error testing Cohere: {e}")
    
    # Test with Hugging Face (if available)
    if HF_AVAILABLE and HFTokenManager.is_token_available():
        print("\n" + "="*70)
        print("Testing with Hugging Face")
        print("="*70)
        
        try:
            hf_pipeline = EnhancedRAGPipeline(
                model_provider="huggingface",
                model_name="microsoft/DialoGPT-medium",  # Example model
                temperature=0.7,
                retrieval_k=3
            )
            
            question = "What is ROS2?"
            result = hf_pipeline.query(question)
            
            print(f"Question: {question}")
            print(f"Answer: {result['answer']}")
            print(f"Sources: {result['num_sources']}")
            
        except Exception as e:
            print(f"Error testing Hugging Face: {e}")
    
    print("\n" + "="*70)
    print("Enhanced RAG Pipeline Test Completed")
    print("="*70)


async def generate_study_tasks(
    topic: Optional[str] = None,
    chapter_id: Optional[str] = None,
    difficulty: str = "medium",
    count: int = 3,
    task_types: Optional[List[str]] = None
) -> List[Dict]:
    """
    Generate AI-powered study tasks based on topic or chapter

    Args:
        topic: Topic to generate tasks for
        chapter_id: Chapter ID to generate tasks for
        difficulty: Difficulty level (easy, medium, hard)
        count: Number of tasks to generate
        task_types: Types of tasks to generate (study, exercise, quiz, review)

    Returns:
        List of task dictionaries with title, description, type, etc.
    """
    try:
        # Initialize RAG pipeline with Cohere
        rag = EnhancedRAGPipeline(model_provider="cohere")

        # Build context query
        context_query = f"Information about {topic or chapter_id}"

        # Get relevant context from RAG
        context_result = rag.ask_question(context_query)
        context = context_result.get("answer", "")

        # Build prompt for task generation
        task_types_str = ", ".join(task_types) if task_types else "study, exercise, quiz, review"

        prompt = f"""Based on the following educational content about {topic or chapter_id},
generate {count} learning tasks for students at {difficulty} difficulty level.

Context:
{context}

Generate tasks of these types: {task_types_str}

For each task, provide:
1. Title (concise, actionable)
2. Description (clear instructions)
3. Task type (study/exercise/quiz/review/reading/practice)
4. Priority (low/medium/high)
5. Estimated duration in minutes

Format your response as a JSON array of tasks. Example:
[
  {{
    "title": "Review Chapter 1: Introduction to ROS2",
    "description": "Read and summarize the key concepts from Chapter 1",
    "task_type": "review",
    "priority": "high",
    "estimated_duration": 30
  }}
]

Generate the tasks now:"""

        # Get AI response
        import json
        ai_response = rag.ask_question(prompt)
        response_text = ai_response.get("answer", "")

        # Try to parse JSON from response
        try:
            # Find JSON array in response
            start_idx = response_text.find("[")
            end_idx = response_text.rfind("]") + 1

            if start_idx != -1 and end_idx != 0:
                json_str = response_text[start_idx:end_idx]
                tasks = json.loads(json_str)
            else:
                # Fallback: create default tasks
                tasks = _create_default_tasks(topic or chapter_id, count, difficulty)
        except json.JSONDecodeError:
            # Fallback: create default tasks
            tasks = _create_default_tasks(topic or chapter_id, count, difficulty)

        return tasks[:count]  # Ensure we return exactly count tasks

    except Exception as e:
        logger.error(f"Error generating AI tasks: {e}")
        # Return default tasks on error
        return _create_default_tasks(topic or chapter_id, count, difficulty)


def _create_default_tasks(topic: str, count: int, difficulty: str) -> List[Dict]:
    """Create default tasks when AI generation fails"""
    tasks = []

    task_templates = [
        {
            "title": f"Study: {topic}",
            "description": f"Read and understand the key concepts about {topic}",
            "task_type": "study",
            "priority": "high",
            "estimated_duration": 30
        },
        {
            "title": f"Exercise: Practice {topic}",
            "description": f"Complete practice exercises related to {topic}",
            "task_type": "exercise",
            "priority": "medium",
            "estimated_duration": 45
        },
        {
            "title": f"Quiz: Test knowledge on {topic}",
            "description": f"Take a quiz to test your understanding of {topic}",
            "task_type": "quiz",
            "priority": "medium",
            "estimated_duration": 20
        },
        {
            "title": f"Review: Summarize {topic}",
            "description": f"Write a summary of what you learned about {topic}",
            "task_type": "review",
            "priority": "low",
            "estimated_duration": 25
        },
        {
            "title": f"Reading: Deep dive into {topic}",
            "description": f"Read additional resources about {topic}",
            "task_type": "reading",
            "priority": "low",
            "estimated_duration": 40
        }
    ]

    return task_templates[:count]


if __name__ == "__main__":
    main()