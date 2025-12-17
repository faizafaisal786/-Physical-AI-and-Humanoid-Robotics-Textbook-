import streamlit as st
from backend.rag import ask_question

st.title("🤖 Physical AI & Humanoid Robotics Chatbot")

question = st.text_input("Apna sawal likho:")

if question:
    answer = ask_question(question)
    st.write(answer)