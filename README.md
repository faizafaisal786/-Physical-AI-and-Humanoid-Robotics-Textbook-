---
title: Physical AI & Humanoid Robotics Chatbot
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.43.0
app_file: deploy_app.py
pinned: false
---

# Physical AI & Humanoid Robotics Textbook - RAG Chatbot

An intelligent chatbot powered by Retrieval-Augmented Generation (RAG) that answers questions about Physical AI and Humanoid Robotics using advanced language models.

## 🌟 Features

- **Smart Question Answering**: Get accurate answers from the textbook content
- **Multiple AI Providers**: Support for both Cohere and Hugging Face models
- **Vector Search**: Efficient document retrieval using ChromaDB
- **Clean Interface**: User-friendly Streamlit web interface

## 🚀 Quick Start

1. Select your preferred AI provider (Cohere recommended)
2. Choose a model from the dropdown
3. Type your question
4. Get instant, context-aware answers!

## 🔑 Configuration

This Space requires API keys to function. Add them in **Space Settings → Repository Secrets**:

- `COHERE_API_KEY`: Get from [Cohere Dashboard](https://dashboard.cohere.com/api-keys)
- `HF_TOKEN`: (Optional) Get from [Hugging Face Settings](https://huggingface.co/settings/tokens)

## 📚 Supported Topics

- ROS2 (Robot Operating System 2)
- Simulation & Digital Twins
- Hardware Basics
- VLA (Vision-Language-Action) Systems
- Advanced AI Control
- Humanoid Robot Design

## 🛠️ Technology Stack

- **Framework**: Streamlit
- **LLM Integration**: LangChain
- **Vector Database**: ChromaDB
- **Embeddings**: Cohere embed-english-v3.0
- **AI Models**: Cohere Command R+, Hugging Face models

## 💡 Sample Questions

- "What is ROS2 and why is it important?"
- "Explain digital twins in robotics"
- "What are VLA systems?"
- "How do humanoid robots work?"

## 🔒 Security

- API tokens are stored securely as Space secrets
- Never exposed in code or logs
- Follow security best practices

## 📖 About the Textbook

This chatbot is based on a comprehensive textbook covering Physical AI and Humanoid Robotics, including theoretical foundations and practical implementations.

---

Built with ❤️ using Streamlit, LangChain, and Cohere
