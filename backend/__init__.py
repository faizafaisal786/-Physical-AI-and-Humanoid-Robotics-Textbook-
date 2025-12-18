"""
Backend package for the Physical AI & Humanoid Robotics textbook RAG system
"""
from .rag import RAGPipeline, ask_question
from .enhanced_rag import EnhancedRAGPipeline, ask_question_with_provider
from .hf_utils import HFTokenManager, get_hf_embeddings, get_hf_model_and_tokenizer
from .config import AppConfig, MODEL_CONFIGS, validate_environment
from .utils import VectorStoreManager

__all__ = [
    # Original RAG components
    "RAGPipeline",
    "ask_question",
    
    # Enhanced RAG components
    "EnhancedRAGPipeline",
    "ask_question_with_provider",
    
    # Hugging Face utilities
    "HFTokenManager",
    "get_hf_embeddings",
    "get_hf_model_and_tokenizer",
    
    # Configuration
    "AppConfig",
    "MODEL_CONFIGS",
    "validate_environment",
    
    # Utils
    "VectorStoreManager"
]