import sys
import os
from pathlib import Path

# Get the absolute path to the project root directory
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

import streamlit as st
from backend.api_model import Groq

# Function to navigate between pages
def navigate_to(page_name):
    st.session_state.current_page = page_name


# Initialize session state for current page and chat history
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Main App Content
if st.session_state.current_page == "Home":
    st.title("Career Advice ChatBot")
    st.subheader("Your guide to building a brighter future")
elif st.session_state.current_page == "Career Resources":
    st.title("Career Resources")
    st.write("Explore resources to boost your career!")
elif st.session_state.current_page == "FAQs":
    st.title("FAQs")
    st.write("Find answers to common questions here.")

# Sidebar Content
with st.sidebar:
    # Input for API Key
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="Enter your Groq API key",
        key="api_key",
    )

    # Sidebar Header and Divider
    st.markdown("## Career Advice Chatbot")
    st.markdown("---")

    # Navigation Section
    st.markdown("### Navigation:")
    if st.button("Home"):
        navigate_to("Home")
    if st.button("Career Resources"):
        navigate_to("Career Resources")
    if st.button("FAQs"):
        navigate_to("FAQs")

    st.markdown("---")

    st.markdown("Contact us at: support@careerbot.ai")
    st.markdown(
        "Disclaimer: This chatbot provides general career\nadvice and does not guarantee job placements."
    )

# Chat Interface (Main Body, Only Visible on Home Page)
if st.session_state.current_page == "Home":
    st.markdown("### Chat with Career Advisor:")
    
    # Initialize Groq if API key is provided
    if api_key:
        advisor = Groq(api_key)
        
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # Chat input
        user_input = st.chat_input("Ask for career advice...")
        
        if user_input:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Get bot response
            with st.chat_message("assistant"):
                response = advisor.get_career_advice(user_input)
                st.write(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
    else:
        st.warning("Please enter your Groq API key in the sidebar to start chatting.")
