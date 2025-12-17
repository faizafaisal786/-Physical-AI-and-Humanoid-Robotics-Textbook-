import streamlit as st
from backend.enhanced_rag import ask_question_with_provider
from backend.config import validate_environment

# Validate environment at startup
validation_result = validate_environment()

st.title("🤖 Physical AI & Humanoid Robotics Chatbot")

# Show available model providers
available_providers = validation_result.get("available_providers", [])
if not available_providers:
    st.warning("⚠️ No model providers configured. Please set either COHERE_API_KEY or HF_TOKEN in your environment variables.")
else:
    st.success(f"✅ Available providers: {', '.join(available_providers)}")

# Model selection
col1, col2 = st.columns(2)

with col1:
    model_provider = st.selectbox(
        "Choose model provider:",
        options=available_providers if available_providers else ["cohere", "huggingface"],
        index=0 if available_providers else 0
    )

with col2:
    if model_provider == "cohere":
        model_name = st.selectbox(
            "Select Cohere model:",
            ["command-r-plus-08-2024", "command-r-08-2024", "command-nightly"],
            index=0
        )
    else:  # HuggingFace
        model_name = st.selectbox(
            "Select Hugging Face model:",
            ["microsoft/DialoGPT-medium", "facebook/blenderbot-400M-distill", "gpt2", "facebook/opt-350m"],
            index=0
        )

question = st.text_input("Apna sawal likho:", placeholder="Enter your question here...")

if question and st.button("Submit Question"):
    with st.spinner(f"Getting answer using {model_provider} model..."):
        try:
            answer = ask_question_with_provider(question, model_provider, model_name)
            st.write("### Answer:")
            st.write(answer)
        except Exception as e:
            st.error(f"Error occurred: {str(e)}")
            st.error("Please check your API keys and model selection.")

# Add configuration info in sidebar
with st.sidebar:
    st.header("About This App")
    st.write("""
    This chatbot uses a Retrieval-Augmented Generation (RAG) system to answer questions
    about Physical AI and Humanoid Robotics based on the textbook content.
    """)

    st.header("Configuration Info")
    st.write(f"Providers: {', '.join(available_providers) if available_providers else 'None configured'}")
    st.write(f"Current Provider: {model_provider}")
    st.write(f"Current Model: {model_name}")

    st.info("ℹ️ Remember to keep your API tokens secure and never share them publicly!")