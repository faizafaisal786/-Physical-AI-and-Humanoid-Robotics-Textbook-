#!/usr/bin/env python3
"""
Deploy RAG Chatbot to Hugging Face Spaces
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and return success status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def main():
    print("🚀 Deploying RAG Chatbot to Hugging Face Spaces")
    print("=" * 50)

    # Check if huggingface_hub is installed
    try:
        import huggingface_hub
    except ImportError:
        print("Installing HuggingFace Hub...")
        if not run_command("pip install huggingface_hub", "Installing huggingface_hub"):
            sys.exit(1)

    # Check if user is logged in
    try:
        from huggingface_hub import whoami
        user = whoami()
        print(f"✅ Logged in as: {user['name']}")
    except:
        print("Please login to Hugging Face first:")
        print("Run: huggingface-cli login")
        sys.exit(1)

    # Create the space
    space_name = "rag-chatbot"
    print(f"Creating Hugging Face Space: {space_name}")

    try:
        from huggingface_hub import create_repo
        create_repo(
            repo_id=space_name,
            repo_type="space",
            space_sdk="streamlit",
            private=False
        )
        print(f"✅ Space created: https://huggingface.co/spaces/{user['name']}/{space_name}")
    except Exception as e:
        print(f"❌ Failed to create space: {e}")
        sys.exit(1)

    print("\n" + "=" * 50)
    print("🎉 Space created successfully!")
    print("\nNext steps:")
    print("1. Go to your space: https://huggingface.co/spaces/[your-username]/rag-chatbot")
    print("2. Go to Settings → Secrets")
    print("3. Add secret: COHERE_API_KEY = your_cohere_api_key")
    print("4. The app will automatically build the database on first run")
    print("\nYour RAG chatbot is now live! 🤖")

if __name__ == "__main__":
    main()