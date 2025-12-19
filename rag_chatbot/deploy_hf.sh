#!/bin/bash
# Deploy RAG Chatbot to Hugging Face Spaces

echo "🚀 Deploying RAG Chatbot to Hugging Face Spaces"
echo ""

# Check if huggingface_hub is installed
if ! command -v huggingface-cli &> /dev/null; then
    echo "Installing HuggingFace CLI..."
    pip install huggingface_hub
fi

# Check if user is logged in
if ! huggingface-cli whoami &> /dev/null; then
    echo "Please login to Hugging Face:"
    huggingface-cli login
fi

echo "Creating Hugging Face Space..."
huggingface-cli create-space rag-chatbot \
    --type space \
    --sdk streamlit \
    --private false \
    --description "RAG Chatbot with Cohere and ChromaDB"

echo ""
echo "Space created! Now you need to:"
echo "1. Go to your Hugging Face Space"
echo "2. Set the COHERE_API_KEY secret"
echo "3. The app will automatically build the database on first run"
echo ""
echo "Your space URL will be: https://huggingface.co/spaces/[your-username]/rag-chatbot"