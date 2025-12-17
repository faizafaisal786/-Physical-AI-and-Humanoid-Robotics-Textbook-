# Physical AI & Humanoid Robotics Textbook - RAG Chatbot

This project implements a Retrieval-Augmented Generation (RAG) chatbot for the Physical AI & Humanoid Robotics textbook. The chatbot can answer questions about the textbook content using advanced language models.

## Features

- Question answering using textbook content
- Support for both Cohere and Hugging Face models
- Vector database for efficient document retrieval
- Streamlit web interface

## Setup Instructions

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - Copy `.env.example` to `.env` and fill in your API keys
   - For Cohere: Get your API key from [Cohere](https://dashboard.cohere.com/api-keys)
   - For Hugging Face: Get your token from [Hugging Face](https://huggingface.co/settings/tokens)

4. Set up the vector database:
   ```bash
   # Run the setup script to create the vector database from textbook content
   # (You'll need to create this script based on your document ingestion process)
   ```

5. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

## Hugging Face Integration

This project includes secure integration with Hugging Face models. To use Hugging Face models:

1. **Get a Hugging Face token**:
   - Go to [Hugging Face Settings → Access Tokens](https://huggingface.co/settings/tokens)
   - Create a new token with appropriate permissions

2. **Configure your environment**:
   - Add your token to `.env` as `HF_TOKEN=your_token_here`
   - Never commit your token to version control

3. **Run with Hugging Face models**:
   - The Streamlit app will allow you to select Hugging Face as a provider
   - Choose from various available models

## Security Best Practices

- **Never commit API tokens** to version control
- Store tokens in environment variables
- Use the `.env.example` file as a template, but don't commit your actual `.env` file
- Regularly rotate your API tokens
- Keep tokens in a secure location, separate from your source code

## Project Structure

- `streamlit_app.py`: Main web interface
- `backend/`: RAG system implementation
  - `rag.py`: Original RAG pipeline with Cohere
  - `enhanced_rag.py`: Enhanced pipeline with both Cohere and Hugging Face support
  - `hf_utils.py`: Hugging Face utilities with secure token management
  - `config.py`: Configuration management
  - `utils.py`: Utility functions
- `requirements.txt`: Python dependencies
- `.env.example`: Environment variable template

## Supported Models

### Cohere Models
- command-r-plus-08-2024
- command-r-08-2024
- command-nightly

### Hugging Face Models
- microsoft/DialoGPT-medium
- facebook/blenderbot-400M-distill
- gpt2
- facebook/opt-350m
- (Plus many others depending on availability)

## Troubleshooting

If you encounter issues:
1. Check that your API keys are correctly set in the `.env` file
2. Ensure required dependencies are installed
3. Verify that your document database has been created
4. Check the console for any error messages