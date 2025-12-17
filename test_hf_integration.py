"""
Test script for Hugging Face integration
Verifies that the secure token management is working correctly
"""
import os
import sys
from backend.hf_utils import HFTokenManager, get_hf_embeddings
from backend.config import validate_environment

def test_hf_token_management():
    """Test Hugging Face token management"""
    print("=" * 60)
    print("Testing Hugging Face Token Management")
    print("=" * 60)

    # Validate environment
    env_status = validate_environment()
    print(f"Environment Status: {env_status}")

    # Test token manager
    print("\n1. Testing HF Token Manager...")
    token_manager = HFTokenManager()

    token_available = HFTokenManager.is_token_available()
    print(f"   Token available: {token_available}")

    if token_available:
        is_valid = token_manager.validate_token()
        print(f"   Token validation: {is_valid}")
        print(f"   Token (masked): {token_manager.get_token()[:5] if token_manager.get_token() else None}...")
    else:
        print("   No token available - this is expected if HF_TOKEN is not set")

    print("\n2. Testing Hugging Face embeddings...")
    try:
        embeddings = get_hf_embeddings()
        print("   [SUCCESS] Successfully created Hugging Face embeddings")

        # Test embedding generation
        test_sentences = ["Hello, world!", "Testing Hugging Face integration."]
        embedded = embeddings.embed_documents(test_sentences)
        print(f"   [SUCCESS] Successfully embedded {len(test_sentences)} sentences")
        print(f"   Embedding dimension: {len(embedded[0]) if embedded else 'N/A'}")

    except Exception as e:
        print(f"   [ERROR] Failed to create embeddings: {e}")

    print("\n" + "=" * 60)
    print("Hugging Face Integration Test Complete")
    print("=" * 60)

def test_config_validation():
    """Test configuration validation"""
    print("\nTesting Configuration Validation...")
    status = validate_environment()

    for key, value in status.items():
        print(f"   {key}: {value}")

    return status

if __name__ == "__main__":
    print("Running Hugging Face Integration Tests...\n")

    # Run tests
    test_hf_token_management()
    config_status = test_config_validation()

    print(f"\nSummary:")
    print(f"- Cohere available: {config_status.get('cohere_available')}")
    print(f"- Hugging Face available: {config_status.get('huggingface_available')}")
    print(f"- Available providers: {config_status.get('available_providers', [])}")

    if not config_status.get('available_providers'):
        print("\n[WARNING] No model providers are configured.")
        print("   Please set either COHERE_API_KEY or HF_TOKEN in your environment.")
        print("   See .env.example for reference.")

    print("\nFor security, remember never to share your API tokens publicly!")