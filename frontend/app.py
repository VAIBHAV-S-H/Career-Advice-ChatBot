import os
import sys
import streamlit as st

sys.path.append("../")
from backend.advice_generator import AdviceGenerator
from backend.conversation_manager import ChatManager


def navigate_to(page_name):
    st.session_state.current_page = page_name


# Page config
st.set_page_config(page_title="Career Advisor", layout="wide")

# Initialize ALL session state variables at the very beginning
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv(
        "GROQ_API_KEY", ""
    )  # Try to get from environment first
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "name_entered" not in st.session_state:
    st.session_state.name_entered = False
if "name" not in st.session_state:
    st.session_state.name = ""
if "chat_manager" not in st.session_state:
    st.session_state.chat_manager = ChatManager()
if "advice_generator" not in st.session_state:
    st.session_state.advice_generator = None  # Will initialize after API key is set
if "initial_message_displayed" not in st.session_state:
    st.session_state.initial_message_displayed = False

# Sidebar
with st.sidebar:
    st.title("Career Advisor")
    api_key = st.text_input(
        "Groq API Key",
        value=st.session_state.api_key,  # Use existing value if present
        type="password",
        placeholder="Enter your Groq API key",
        key="api_key_input",
    )

    if api_key:
        st.session_state.api_key = api_key
        # Initialize advice generator when API key is set
        if st.session_state.advice_generator is None:
            st.session_state.advice_generator = AdviceGenerator(api_key=api_key)

    # Navigation Section
    st.markdown("### Navigation:")
    if st.button("Home"):
        navigate_to("Home")
    if st.button("FAQs"):
        navigate_to("FAQs")

    st.markdown("---")
    st.markdown("### About")
    st.write("I'm your AI Career Advisor specialized in engineering fields.")

    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.name_entered = False
        st.session_state.chat_manager.clear_history()
        st.session_state.initial_message_displayed = False

    st.markdown("---")
    st.markdown("Contact us at: support@careerbot.ai")
    st.markdown(
        "Disclaimer: This chatbot provides general career\nadvice and does not guarantee job placements."
    )

# Check for API key before proceeding
if not st.session_state.api_key:
    st.warning("Please enter your Groq API Key in the sidebar to continue.")
    st.stop()

# Main content based on current page
if st.session_state.current_page == "Home":
    st.title("Career Advisor Chat")

    # Name input if not already entered
    if not st.session_state.get("name_entered", False):
        name = st.text_input(
            "Name:",
            placeholder="Enter your name",
            value=st.session_state.get("name", ""),
        )
        if name and name != st.session_state.get("name", ""):
            st.session_state.name = name
            st.session_state.name_entered = True

            # Check if the initial message has already been displayed
            if not st.session_state.initial_message_displayed:
                initial_message = f"""Hello {name}! I'm your AI Career Advisor. I can help you with:
                \n- Career guidance and planning
                \n- Skill development advice
                \n- Job search strategies
                \n- Industry insights
                \nWhat would you like to discuss about your career?"""

                # Add the initial message to messages only if it's not already there
                if not any(
                    msg.get("role") == "assistant" and "Hello" in msg.get("content", "")
                    for msg in st.session_state.messages
                ):
                    st.session_state.messages.append(
                        {"role": "assistant", "content": initial_message}
                    )

                # Mark the initial message as displayed
                st.session_state.initial_message_displayed = True

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if st.session_state.name_entered:
        if prompt := st.chat_input("Ask me about your career..."):
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("assistant"):
                st.session_state.chat_manager.user_history(prompt)
                response = st.session_state.advice_generator.generate_advice(
                    history=st.session_state.chat_manager.get_history(),
                    user_input=prompt,
                )
                st.session_state.chat_manager.bot_history(response)
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

elif st.session_state.current_page == "FAQs":
    st.title("Frequently Asked Questions")
    st.markdown("""
    ### Common Questions
    1. How can I use this Career Advisor?
    2. What types of career advice can I get?
    3. How do I get started with career planning?
    
    ### Getting Started
    Simply enter your name and start chatting with our AI Career Advisor. 
    Ask any questions related to your engineering career path!
    """)
