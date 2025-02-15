import streamlit as st
import os
from groq import Groq

# Load API key from environment variable
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("API key is missing! Set the GROQ_API_KEY environment variable.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=api_key)

st.title("Chat with AI 🤖")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Display previous messages
for message in st.session_state.messages:
    if message["role"] != "system":  # Don't show system messages
        with st.chat_message(message["role"]):
            st.write(message["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Append user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get response from LLM
    response = client.chat.completions.create(
        messages=st.session_state.messages,
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        max_completion_tokens=1024,
    ).choices[0].message.content

    # Append assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display assistant response
    with st.chat_message("assistant"):
        st.write(response)

# Optional: Add a "Clear Chat" button
if st.button("Clear Chat"):
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    st.experimental_rerun()
