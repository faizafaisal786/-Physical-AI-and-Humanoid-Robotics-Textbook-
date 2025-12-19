---
title: RAG Chatbot
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.31.0
app_file: app.py
pinned: false
---

# RAG Chatbot - Physical AI and Humanoid Robotics Textbook

A Retrieval-Augmented Generation (RAG) chatbot built with Cohere, ChromaDB, and Streamlit.

## Features

- 🤖 **Cohere Command-R-Plus** for intelligent responses
- 📚 **ChromaDB** for efficient vector storage
- 🔍 **Semantic search** through your documents
- 💬 **Interactive Streamlit** interface
- 📝 **Text/Markdown** document support
- 🎯 **Source citations** for answers

## How it works

This chatbot uses:
- **Cohere's Command-R-Plus model** for generating responses
- **ChromaDB** as the vector database for document storage
- **RAG (Retrieval-Augmented Generation)** to provide accurate answers based on your documents

## Setup

The app will automatically set up the vector database on first run using the documents in the `docs/` folder.

## Deployment to Hugging Face

### Automatic Deployment

Run the deployment script:

```bash
python deploy_hf.py
```

This will:
- Create a new Hugging Face Space
- Upload your code
- Set up the environment

### Manual Deployment

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Choose:
   - **Space SDK**: Streamlit
   - **Space Name**: rag-chatbot (or any name you prefer)
4. Upload all files from this directory to your Space
5. In your Space settings, add the secret:
   - **Name**: `COHERE_API_KEY`
   - **Value**: Your Cohere API key

### Important Notes

- **Pre-built database**: The vector database (`chroma_db/`) is pre-built and included in the repository
- **Secret required**: Add `COHERE_API_KEY` in Space Settings > Repository secrets
- No rebuild needed: Database is ready to use immediately
- Make sure your Cohere API key has sufficient credits

## Local Development

To run locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Set up database
python setup_db.py

# Run the app
streamlit run app.py
```

## Usage

### Run the Chatbot

```bash
streamlit run app.py
```

The chatbot will open in your browser at `http://localhost:8501`

### Rebuild Database

If you add new documents or want to rebuild:

```bash
python setup_db.py --force
```

### Use Custom Document Directory

```bash
python setup_db.py --docs-dir /path/to/your/documents
```

## Project Structure

```
rag_chatbot/
├── app.py                    # Streamlit chatbot interface
├── rag_pipeline.py          # RAG pipeline (retrieval + generation)
├── vector_store.py          # ChromaDB vector store manager
├── ingest_documents.py      # Document loading and processing
├── setup_db.py              # Database setup script
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment file
├── .env                    # Your environment variables (create this)
└── chroma_db/              # ChromaDB storage (auto-created)
```

## How It Works

1. **Document Ingestion**: Loads markdown/text files and splits them into chunks
2. **Embedding**: Uses Cohere's embedding model to create vector embeddings
3. **Storage**: Stores embeddings in ChromaDB for fast retrieval
4. **Retrieval**: When you ask a question, finds relevant document chunks
5. **Generation**: Uses Cohere's Command-R-Plus model to generate answers based on retrieved context
6. **Citation**: Shows source documents with relevance scores

## Configuration

### Environment Variables

Edit `.env` file:

```env
COHERE_API_KEY=your_cohere_api_key_here
```

### Settings in App

- **Response Creativity**: Control temperature (0=focused, 1=creative)
- **Number of Sources**: How many documents to retrieve per query

### Model Settings

Edit `rag_pipeline.py` to change:

```python
pipeline = RAGPipeline(
    model_name="command-r-plus-08-2024",
    temperature=0.7,
    max_tokens=500,
    retrieval_k=5
)
```

## Supported Document Types

- Markdown files (`.md`)
- Text files (`.txt`)

Documents are loaded recursively from the specified directory.

## Troubleshooting

### "COHERE_API_KEY not set" Error

Make sure you:
1. Created `.env` file from `.env.example`
2. Added your actual Cohere API key
3. API key is valid and has credits

### "No documents found" Error

- Check that your documents directory exists
- Ensure it contains `.md` or `.txt` files
- Use `--docs-dir` to specify correct path

### "Vector store not initialized" Error

Run the setup script first:
```bash
python setup_db.py
```

## Cost Estimation

Cohere API costs (approximate):
- **Embeddings**: Cohere offers generous free tier
- **Command-R-Plus**: Check Cohere pricing for current rates

For typical usage:
- Initial setup: One-time embedding cost
- Per query: Based on tokens used

## Tips

- Use specific questions for better results
- Check source citations to verify answers
- Adjust "Number of Sources" if answers lack context
- Lower temperature (0.3-0.5) for factual questions
- Higher temperature (0.7-0.9) for creative questions

## License

MIT License

## Support

For issues or questions, please check:
- Cohere API documentation: https://docs.cohere.com/
- ChromaDB documentation: https://docs.trychroma.com/
- Streamlit documentation: https://docs.streamlit.io/
