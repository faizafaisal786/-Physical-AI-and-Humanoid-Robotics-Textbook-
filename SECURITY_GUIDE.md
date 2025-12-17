# Secure Hugging Face Token Implementation Guide

This document explains how to use the secure Hugging Face token management system implemented in the Physical AI & Humanoid Robotics Textbook RAG Chatbot.

## Overview

The implementation provides secure handling of Hugging Face tokens through:

1. Environment variable-based token storage
2. Secure token validation
3. Masked token display
4. Automatic token setup for transformers library
5. Proper error handling

## Components

### 1. HFTokenManager (`backend/hf_utils.py`)

The `HFTokenManager` class handles all token-related operations:

- Reads tokens from environment variables (`HF_TOKEN` or `HUGGING_FACE_TOKEN`)
- Validates tokens by attempting to log in to Hugging Face Hub
- Provides secure access to tokens
- Includes validation methods

### 2. Secure Embeddings (`backend/hf_utils.py`)

The `get_hf_embeddings()` function creates Hugging Face embeddings while respecting token security:

- Automatically uses tokens from environment variables when available
- Falls back to public models when no token is provided
- Maintains security by not exposing tokens in the code

### 3. Enhanced RAG Pipeline (`backend/enhanced_rag.py`)

The `EnhancedRAGPipeline` supports both Cohere and Hugging Face models:

- Configurable to use either model provider
- Securely handles tokens based on the selected provider
- Maintains the same interface regardless of provider

### 4. Configuration Management (`backend/config.py`)

The `AppConfig` class manages application configuration:

- Determines available providers based on environment variables
- Validates configuration at startup
- Provides centralized configuration access

## Security Features

1. **Environment Variable Only**: Tokens are only read from environment variables, never hardcoded
2. **Token Validation**: Automatic validation of tokens upon initialization
3. **Masked Display**: Sensitive tokens are masked when displayed for debugging
4. **Secure Defaults**: Fallback mechanisms when tokens are not available
5. **Error Handling**: Proper error handling without exposing sensitive information

## Usage

### Setting up Environment Variables

Create a `.env` file in your project root:

```
HF_TOKEN=your_huggingface_token_here
COHERE_API_KEY=your_cohere_api_key_here  # if using Cohere
```

Then add `.env` to your `.gitignore` to prevent committing tokens:

```
echo '.env' >> .gitignore
```

### Using the Token Manager

```python
from backend.hf_utils import HFTokenManager

# Initialize the token manager
token_manager = HFTokenManager()

# Check if a token is available
if HFTokenManager.is_token_available():
    print("Token is available")
    
    # Validate the token
    if token_manager.validate_token():
        print("Token is valid")
    else:
        print("Token is invalid")
else:
    print("No token available")
```

### Creating Hugging Face Embeddings

```python
from backend.hf_utils import get_hf_embeddings

# Create embeddings (will use token from environment if available)
embeddings = get_hf_embeddings()

# Use for embedding documents
documents = ["Hello, world!", "This is a test"]
embedded = embeddings.embed_documents(documents)
```

## Best Practices

1. **Never hardcode tokens** in source code
2. **Use environment variables** for token storage
3. **Add .env files to .gitignore** to prevent committing tokens
4. **Validate tokens** before using them for API calls
5. **Mask tokens** when displaying for debugging purposes
6. **Handle missing tokens gracefully** with appropriate error messages
7. **Use different tokens** for development and production environments

## Testing

Use the provided test scripts to verify your implementation:

```bash
# Test Hugging Face integration
python test_hf_integration.py

# Test enhanced RAG pipeline
python test_enhanced_rag.py

# Verify the entire implementation
python verify_implementation.py

# Demonstrate security features
python demonstrate_security.py
```

## Troubleshooting

### Token Validation Fails

- Ensure your token is valid and has the necessary permissions
- Check that the token is correctly set in the environment
- Verify you're using the correct environment variable name

### Module Import Errors

- Make sure all required packages are installed (`pip install -r requirements.txt`)
- Ensure the `sentence-transformers` package is installed for embeddings

### Missing Environment Variables

- Create a `.env` file with the required variables
- Make sure to call `load_dotenv()` before using environment variables
- Verify the `.env` file is in the correct location

## Security Verification

The implementation includes several security measures:

- [x] Tokens stored only in environment variables
- [x] No hardcoded tokens in source code
- [x] Secure token masking for display
- [x] Proper validation of tokens
- [x] Error handling without information leakage
- [x] Automatic token setup for transformers
- [x] Fallback mechanisms for missing tokens