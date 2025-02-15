# app.py
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
        {"role": "system", "content": '''You are tasked with designing an AI-powered language learning platform that enhances learning and retention through personalized content and adaptive exercises. The platform must incorporate two key personalization factors:

        Weakness-Based Personalization:

        Continuously analyze learners' performance to identify weaknesses (e.g., grammar, vocabulary, pronunciation, listening comprehension).
        Generate customized exercises targeting these areas.
        Provide targeted, dynamic feedback and progressively challenging tasks to ensure steady improvement.
        Interest-Based Personalization:

        Gather and analyze data on learners’ interests (e.g., favorite topics, hobbies, music, movies, professional interests).
        Generate exercises, reading materials, and conversation prompts that incorporate these themes to boost engagement and real-world language application.
        Additionally, ensure the platform includes the following features:

        Interactive Exercises: Engage users with various formats such as text-based lessons, audio-visual content, and gamified challenges.
        AI-Generated Feedback: Offer real-time insights and tips based on performance.
        Real-Time Progress Tracking: Monitor and display learners' advancement to motivate continued learning.
        Adaptive Difficulty Levels: Automatically adjust the complexity of exercises based on the learner’s evolving skill level.
        Your Task: Develop a comprehensive design for this language learning platform, detailing how each component (weakness-based and interest-based personalization, interactive exercises, feedback systems, progress tracking, and adaptive difficulty) will function and integrate. Explain how the platform will gather and utilize data to create a truly personalized learning experience that caters to individual user needs and preferences.

'''}
    ]

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

# Display previous messages
for message in st.session_state.messages:
    if message["role"] != "system":  # Don't show system messages
        with st.chat_message(message["role"]):
            st.write(message["content"])

# # Optional: Add a "Clear Chat" button
# if st.button("Clear Chat"):
#     st.session_state.messages = [
#         {"role": "system", "content": "You are a helpful assistant."}
#     ]
#     st.experimental_rerun()

