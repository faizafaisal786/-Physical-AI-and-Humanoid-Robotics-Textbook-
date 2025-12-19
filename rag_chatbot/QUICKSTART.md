# Quick Start Guide - RAG Chatbot

## Current Installation Issue

There's a temporary file lock issue with ChromaDB installation. Here are the solutions:

### Solution 1: Restart and Install (Recommended)

1. **Close all Python processes and terminals**
2. **Restart your computer** (to release any file locks)
3. **Open a new terminal** and run:

```bash
cd "C:\Users\HDD BANK\Desktop\book\rag_chatbot"
pip install -r requirements.txt
```

### Solution 2: Manual Installation

If the above doesn't work, install packages one by one:

```bash
cd "C:\Users\HDD BANK\Desktop\book\rag_chatbot"

# Core packages (already installed)
pip install openai streamlit python-dotenv tiktoken

# ChromaDB (the problematic one)
pip install chromadb

# LangChain packages
pip install langchain langchain-openai langchain-community
```

### Solution 3: Alternative - Use FAISS Instead of ChromaDB

If ChromaDB continues to have issues, I can create a version using FAISS (simpler, no lock issues):

```bash
pip install faiss-cpu langchain-openai streamlit
```

## Setup Steps (After Installation)

### 1. Set Up Environment Variables

```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your OpenAI API key
notepad .env
```

Add your API key:
```
OPENAI_API_KEY=sk-your-key-here
```

Get your key from: https://platform.openai.com/api-keys

### 2. Create the Vector Database

```bash
python setup_db.py
```

This will:
- Load all markdown/text files from `../docusaurus_textbook/docs`
- Generate embeddings
- Store in ChromaDB
- Takes 2-5 minutes depending on document size

### 3. Run the Chatbot

```bash
streamlit run app.py
```

The chatbot will open in your browser at `http://localhost:8501`

## Troubleshooting

### "ModuleNotFoundError: No module named 'chromadb'"

Chromadb didn't install. Try:
```bash
pip install --force-reinstall chromadb
```

### "OPENAI_API_KEY not found"

You didn't set up the `.env` file. See step 1 above.

### "Vector store not initialized"

You didn't run `python setup_db.py`. See step 2 above.

### Still Having Issues?

Let me know and I can:
1. Create a FAISS version (simpler)
2. Create a version that doesn't need a vector database
3. Help debug specific errors

## What's Already Done

✅ All code files created:
- `app.py` - Streamlit chatbot interface
- `rag_pipeline.py` - RAG logic
- `vector_store.py` - ChromaDB integration
- `ingest_documents.py` - Document processing
- `setup_db.py` - Database setup script
- `requirements.txt` - Dependencies
- `.env.example` - Environment template
- `README.md` - Full documentation

✅ Project structure ready
✅ All modules configured

❌ Dependencies installation (blocked by file lock)

## Next Steps

1. Fix the installation issue using Solution 1 or 2 above
2. Set up your OpenAI API key
3. Run `python setup_db.py` to create the database
4. Run `streamlit run app.py` to start chatting!

---

**Need help?** Let me know which solution you'd like to try!
