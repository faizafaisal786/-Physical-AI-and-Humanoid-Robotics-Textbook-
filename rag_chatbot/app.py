"""
Streamlit RAG Chatbot Application
Interactive chatbot interface for querying documents
"""
import streamlit as st
import os
from dotenv import load_dotenv
from rag_pipeline import RAGPipeline

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextInput > div > div > input {
        font-size: 16px;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
    }
    .bot-message {
        background-color: #f5f5f5;
        border-left: 5px solid #4caf50;
    }
    .source-doc {
        background-color: #fff3e0;
        padding: 0.5rem;
        border-radius: 0.3rem;
        margin-top: 0.5rem;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_pipeline():
    """Initialize RAG pipeline (cached to avoid reloading)"""
    try:
        import os
        
        # Check if database exists
        db_path = "./chroma_db"
        db_exists = os.path.exists(db_path) and os.path.isdir(db_path)
        
        if db_exists:
            # Check if database directory is not empty
            try:
                db_contents = os.listdir(db_path)
                if not db_contents:
                    db_exists = False
            except:
                db_exists = False
        
        # If database doesn't exist, try to create it (only for small datasets)
        if not db_exists:
            docs_path = "./docs"
            if os.path.exists(docs_path) and os.path.isdir(docs_path):
                try:
                    docs_list = os.listdir(docs_path)
                    # Only try auto-setup if there are documents and it's a small set
                    if docs_list:
                        st.info("🔄 Database not found. Attempting to create it... This may take a few minutes.")
                        import subprocess
                        result = subprocess.run(
                            ["python", "setup_db.py", "--docs-dir", docs_path], 
                            capture_output=True, 
                            text=True,
                            timeout=600  # 10 minute timeout
                        )
                        if result.returncode != 0:
                            st.error(f"⚠️ Auto-setup failed. Please build database locally and commit it.")
                            return None, f"Database setup failed: {result.stderr[:500]}"
                        # Verify database was created
                        if not os.path.exists(db_path) or not os.listdir(db_path):
                            return None, "Database creation did not complete successfully"
                except subprocess.TimeoutExpired:
                    st.error("⏱️ Database creation timed out. For large datasets, please pre-build the database locally.")
                    return None, "Database setup timeout - please build locally"
                except Exception as e:
                    st.error(f"⚠️ Could not auto-create database: {str(e)}")
                    return None, f"Database auto-setup error: {str(e)}"
            else:
                st.error("⚠️ Database not found and no documents directory available.")
                return None, "Database not found. Please ensure chroma_db/ is committed or docs/ directory exists."
        
        # Initialize pipeline
        pipeline = RAGPipeline(
            model_name="command-r-plus-08-2024",
            temperature=0.7,
            max_tokens=500,
            retrieval_k=5
        )
        return pipeline, None
    except Exception as e:
        return None, str(e)


def display_message(role, content, sources=None):
    """Display a chat message with optional sources"""
    css_class = "user-message" if role == "user" else "bot-message"
    icon = "👤" if role == "user" else "🤖"

    st.markdown(f"""
        <div class="chat-message {css_class}">
            <div><strong>{icon} {role.title()}</strong></div>
            <div style="margin-top: 0.5rem;">{content}</div>
        </div>
    """, unsafe_allow_html=True)

    # Display sources if available
    if sources and role == "assistant":
        with st.expander(f"📚 View {len(sources)} Source Documents"):
            for i, source in enumerate(sources, 1):
                st.markdown(f"""
                    <div class="source-doc">
                        <strong>Source {i}</strong> (Relevance: {source['relevance_score']:.4f})<br>
                        <em>File: {source['source'].split('/')[-1]}</em><br>
                        {source['content'][:150]}...
                    </div>
                """, unsafe_allow_html=True)


def main():
    """Main application"""

    # Sidebar
    with st.sidebar:
        st.title("🤖 RAG Chatbot")
        st.markdown("---")

        st.markdown("""
        ### About
        This chatbot uses:
        - **Cohere Command-R-Plus (08-2024)** for responses
        - **ChromaDB** for document storage
        - **RAG** (Retrieval-Augmented Generation)

        ### How to use
        1. Type your question
        2. Press Enter or click Send
        3. View answer with sources
        """)

        st.markdown("---")

        # Settings
        st.subheader("⚙️ Settings")

        # Temperature slider
        temperature = st.slider(
            "Response Creativity",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher values = more creative responses"
        )

        # Number of sources
        num_sources = st.slider(
            "Number of Sources",
            min_value=1,
            max_value=10,
            value=5,
            help="Documents to retrieve per query"
        )

        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.markdown("---")

        # System info
        with st.expander("ℹ️ System Info"):
            api_key_set = "✅" if os.getenv("COHERE_API_KEY") else "❌"
            st.markdown(f"""
            - Cohere API Key: {api_key_set}
            - Model: command-r-plus-08-2024
            - Vector DB: ChromaDB
            """)

    # Main content
    st.title("💬 RAG Chatbot")
    st.markdown("Ask questions about your documents!")

    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Initialize pipeline
    pipeline, error = initialize_pipeline()

    if error:
        st.error(f"⚠️ Error initializing chatbot: {error}")
        st.info("Make sure you have set up the vector database. Run: `python setup_db.py`")
        return

    if not pipeline:
        st.error("⚠️ Failed to initialize RAG pipeline")
        return

    # Display chat history
    for message in st.session_state.messages:
        display_message(
            message["role"],
            message["content"],
            message.get("sources")
        )

    # Chat input
    user_input = st.chat_input("Type your question here...")

    if user_input:
        # Add user message to history
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        # Display user message
        display_message("user", user_input)

        # Get response from pipeline
        with st.spinner("🤔 Thinking..."):
            # Update pipeline settings
            pipeline.llm.temperature = temperature
            pipeline.retrieval_k = num_sources

            # Query pipeline
            result = pipeline.query(user_input)

            # Check for errors
            if result.get("error"):
                response_text = result["answer"] + f"\n\n⚠️ Error: {result['error']}"
                sources = []
            else:
                response_text = result["answer"]
                sources = result.get("source_documents", [])

        # Add assistant message to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": response_text,
            "sources": sources
        })

        # Display assistant message
        display_message("assistant", response_text, sources)

        # Rerun to update the chat
        st.rerun()

    # Welcome message
    if len(st.session_state.messages) == 0:
        st.info("👋 Welcome! Ask me anything about your documents.")

        # Example questions
        st.markdown("### 💡 Example Questions")
        col1, col2 = st.columns(2)

        example_questions = [
            "What is ROS2?",
            "Explain humanoid robotics",
            "What are VLA models?",
            "How does simulation work?"
        ]

        for i, question in enumerate(example_questions):
            col = col1 if i % 2 == 0 else col2
            if col.button(question, key=f"example_{i}", use_container_width=True):
                st.session_state.messages.append({
                    "role": "user",
                    "content": question
                })
                st.rerun()


if __name__ == "__main__":
    main()
