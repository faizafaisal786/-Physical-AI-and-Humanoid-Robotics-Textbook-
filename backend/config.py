"""
Configuration module for the RAG application
Manages settings for both Cohere and Hugging Face models
"""
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

# Model configurations
MODEL_CONFIGS = {
    "cohere": {
        "models": [
            "command-r-plus-08-2024",
            "command-r-08-2024",
            "command-nightly",  # Updated nightly model
        ],
        "default_model": "command-r-plus-08-2024",
        "requires_api_key": "COHERE_API_KEY",
    },
    "huggingface": {
        "models": [
            "microsoft/DialoGPT-medium",
            "facebook/blenderbot-400M-distill",
            "gpt2",
            "EleutherAI/gpt-j-6B",  # Larger model option
            "facebook/opt-350m",    # Alternative model
        ],
        "default_model": "microsoft/DialoGPT-medium",
        "requires_token": "HF_TOKEN",
    }
}


class AppConfig:
    """Application configuration class"""
    
    def __init__(self):
        self.cohere_api_key = os.getenv("COHERE_API_KEY")
        self.hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGING_FACE_TOKEN")
        self.chroma_db_path = os.getenv("CHROMA_DB_PATH", "./chroma_db")
        self.collection_name = os.getenv("COLLECTION_NAME", "rag_chatbot")
        
        # Model settings
        self.default_provider = os.getenv("DEFAULT_MODEL_PROVIDER", "cohere")
        self.default_model = os.getenv("DEFAULT_MODEL", MODEL_CONFIGS[self.default_provider]["default_model"])
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "500"))
        self.retrieval_k = int(os.getenv("RETRIEVAL_K", "5"))
    
    def is_cohere_available(self) -> bool:
        """Check if Cohere is available and properly configured"""
        return bool(self.cohere_api_key)
    
    def is_huggingface_available(self) -> bool:
        """Check if Hugging Face is available and properly configured"""
        return bool(self.hf_token)
    
    def get_available_providers(self) -> list:
        """Get list of available model providers based on configuration"""
        providers = []
        if self.is_cohere_available():
            providers.append("cohere")
        if self.is_huggingface_available():
            providers.append("huggingface")
        return providers
    
    def validate_config(self) -> Dict[str, Any]:
        """Validate the configuration and return status"""
        status = {
            "cohere_available": self.is_cohere_available(),
            "huggingface_available": self.is_huggingface_available(),
            "available_providers": self.get_available_providers(),
            "chroma_db_path": self.chroma_db_path,
            "collection_name": self.collection_name,
        }
        
        if not status["available_providers"]:
            status["warning"] = "No model providers configured. Please set either COHERE_API_KEY or HF_TOKEN."
        else:
            status["info"] = f"Configured providers: {', '.join(status['available_providers'])}"
        
        return status


# Global configuration instance
config = AppConfig()


def get_default_provider() -> str:
    """Get the default model provider based on available credentials"""
    if config.is_cohere_available():
        return "cohere"
    elif config.is_huggingface_available():
        return "huggingface"
    else:
        raise ValueError("No model provider credentials available. Please set either COHERE_API_KEY or HF_TOKEN.")


def get_default_model(provider: Optional[str] = None) -> str:
    """Get the default model for the specified or configured provider"""
    if provider is None:
        provider = get_default_provider()
    
    return MODEL_CONFIGS[provider]["default_model"]


def get_model_list(provider: str) -> list:
    """Get list of available models for the specified provider"""
    return MODEL_CONFIGS[provider]["models"]


def validate_environment() -> Dict[str, Any]:
    """Validate the environment configuration"""
    return config.validate_config()


if __name__ == "__main__":
    # Print configuration status
    print("RAG Application Configuration:")
    print("-" * 40)
    
    validation_result = validate_environment()
    
    for key, value in validation_result.items():
        print(f"{key}: {value}")
    
    print("\nEnvironment variables status:")
    print(f"COHERE_API_KEY set: {'Yes' if config.cohere_api_key else 'No'}")
    print(f"HF_TOKEN set: {'Yes' if config.hf_token else 'No'}")
    print(f"Default provider: {config.default_provider}")
    print(f"Default model: {config.default_model}")