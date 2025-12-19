"""
Test script to verify RAG chatbot is working properly
"""
from backend.enhanced_rag import ask_question_with_provider

print("="*70)
print("Testing RAG Chatbot")
print("="*70)

# Test with Cohere
print("\n[1] Testing with Cohere model...")
print("-" * 70)
question = "What is ROS2?"
print(f"Question: {question}")
print("\nGenerating answer...")

try:
    answer = ask_question_with_provider(question, "cohere", "command-r-plus-08-2024")
    print(f"\nAnswer:\n{answer}")
    print("\n[SUCCESS] Cohere model working!")
except Exception as e:
    print(f"\n[ERROR] Cohere test failed: {e}")

# Test with HuggingFace
print("\n" + "="*70)
print("[2] Testing with HuggingFace model...")
print("-" * 70)
question = "What are humanoid robots?"
print(f"Question: {question}")
print("\nGenerating answer...")

try:
    answer = ask_question_with_provider(question, "huggingface", "microsoft/DialoGPT-medium")
    print(f"\nAnswer:\n{answer}")
    print("\n[SUCCESS] HuggingFace model working!")
except Exception as e:
    print(f"\n[ERROR] HuggingFace test failed: {e}")

print("\n" + "="*70)
print("Testing Complete!")
print("="*70)
