---
title: Physical AI and Humanoid Robotics Textbook
emoji: 🤖
colorFrom: blue
colorTo: red
sdk: streamlit
sdk_version: 1.31.0
app_file: streamlit_app.py
pinned: false
short_description: AI-powered robotics textbook with RAG chatbot
tags:
- streamlit
- robotics
- ai
- education
- rag
- chatbot
---

# Physical AI and Humanoid Robotics Textbook

An interactive textbook for learning about Physical AI and Humanoid Robotics, featuring a RAG-powered chatbot for querying the content.

## Project Structure

```
Physical-AI-and-Humanoid-Robotics-Textbook/
│
├── streamlit_app.py        # Main Streamlit frontend for the RAG chatbot
├── backend/                # Backend logic for RAG processing
│   ├── rag.py             # RAG pipeline implementation
│   └── utils.py           # Vector store utilities
│
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .gitignore             # Git ignore rules
```

## Features

- **Interactive Chatbot**: Ask questions about robotics concepts using natural language
- **RAG Technology**: Retrieval-Augmented Generation for accurate, context-aware answers
- **Document Sources**: View source documents and relevance scores for transparency
- **Modular Architecture**: Clean separation between frontend and backend logic

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your Cohere API key:
   ```bash
   export COHERE_API_KEY="your-api-key-here"
   ```

3. Run the application:
   ```bash
   streamlit run streamlit_app.py
   ```

## Technologies Used

- **Frontend**: Streamlit
- **Backend**: Python
- **LLM**: Cohere Command-R-Plus
- **Vector Database**: ChromaDB
- **Embeddings**: Cohere Embeddings
