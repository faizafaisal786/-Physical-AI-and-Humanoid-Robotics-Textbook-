"""
Hugging Face Utilities Module
Securely manages Hugging Face token and provides utility functions
"""
import os
import logging
from typing import Optional
from dotenv import load_dotenv
from huggingface_hub import login, whoami
from transformers import AutoTokenizer, AutoModel
from langchain_huggingface import HuggingFaceEmbeddings

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HFTokenManager:
    """Manages Hugging Face token securely"""

    def __init__(self):
        """Initialize the token manager and validate the token if present"""
        self.token = os.getenv("HF_TOKEN") or os.getenv("HUGGING_FACE_TOKEN")
        
        if self.token:
            self.validate_token()
        else:
            logger.warning("No Hugging Face token found in environment variables")
    
    def validate_token(self) -> bool:
        """Validate the Hugging Face token by attempting to log in"""
        try:
            login(token=self.token)
            user_info = whoami()
            logger.info(f"Hugging Face token validated for user: {user_info['name']}")
            return True
        except Exception as e:
            logger.error(f"Failed to validate Hugging Face token: {e}")
            return False
    
    def get_token(self) -> Optional[str]:
        """Get the Hugging Face token from environment variables"""
        return self.token
    
    @staticmethod
    def is_token_available() -> bool:
        """Check if a Hugging Face token is available in environment variables"""
        return bool(os.getenv("HF_TOKEN") or os.getenv("HUGGING_FACE_TOKEN"))
    
    @staticmethod
    def setup_token_for_transformers():
        """Set up the token for use with the transformers library"""
        token = os.getenv("HF_TOKEN") or os.getenv("HUGGING_FACE_TOKEN")
        if token:
            login(token=token)
            logger.info("Hugging Face token set up for transformers library")
        else:
            logger.warning("No Hugging Face token available")


def get_hf_embeddings(
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    encode_kwargs: Optional[dict] = None
) -> HuggingFaceEmbeddings:
    """
    Get Hugging Face embeddings with secure token management
    
    Args:
        model_name: Name of the model to use for embeddings
        encode_kwargs: Additional arguments for encoding
        
    Returns:
        HuggingFaceEmbeddings instance
    """
    if encode_kwargs is None:
        encode_kwargs = {'normalize_embeddings': True}
    
    # Set up token if available
    if HFTokenManager.is_token_available():
        HFTokenManager.setup_token_for_transformers()
    
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            encode_kwargs=encode_kwargs
        )
        logger.info(f"Initialized Hugging Face embeddings with model: {model_name}")
        return embeddings
    except Exception as e:
        logger.error(f"Failed to initialize Hugging Face embeddings: {e}")
        raise


def get_hf_model_and_tokenizer(
    model_name: str = "gpt2",
    trust_remote_code: bool = False
):
    """
    Get Hugging Face model and tokenizer with secure token management
    
    Args:
        model_name: Name of the model to load
        trust_remote_code: Whether to trust remote code in the model
        
    Returns:
        Tuple of (model, tokenizer)
    """
    # Set up token if available
    if HFTokenManager.is_token_available():
        HFTokenManager.setup_token_for_transformers()
    
    try:
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=trust_remote_code
        )
        
        # Load model
        model = AutoModel.from_pretrained(
            model_name,
            trust_remote_code=trust_remote_code
        )
        
        # Add padding token if not present (needed for some models)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        logger.info(f"Loaded model and tokenizer: {model_name}")
        return model, tokenizer
        
    except Exception as e:
        logger.error(f"Failed to load model and tokenizer: {e}")
        raise


def main():
    """Test Hugging Face utilities"""
    print("Testing Hugging Face Utilities...")
    
    # Test token manager
    token_manager = HFTokenManager()
    token_available = HFTokenManager.is_token_available()
    
    print(f"Hugging Face token available: {token_available}")
    
    if token_available:
        print("Validating token...")
        is_valid = token_manager.validate_token()
        print(f"Token validation result: {is_valid}")
    else:
        print("No token available in environment variables.")
        print("To use Hugging Face features, set HF_TOKEN in your .env file.")
    
    # Test embeddings if token is available
    if token_available:
        print("\nTesting Hugging Face embeddings...")
        try:
            embeddings = get_hf_embeddings()
            test_texts = ["Hello, world!", "This is a test embedding."]
            embedding_results = embeddings.embed_documents(test_texts)
            print(f"Successfully generated embeddings for {len(test_texts)} texts")
            print(f"Embedding dimension: {len(embedding_results[0])}")
        except Exception as e:
            print(f"Error with embeddings: {e}")
    
    print("\nHugging Face utilities test completed.")


if __name__ == "__main__":
    main()