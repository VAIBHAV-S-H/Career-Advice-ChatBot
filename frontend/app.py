import os
import sys
import streamlit as st

sys.path.append("../")
from backend.advice_generator import AdviceGenerator
from backend.conversation_manager import ChatManager


def reset_session_state():
    """
    Completely reset all session state variables to their initial state.
    This effectively creates a fresh start for the application.
    Preserves the Groq API key.
    """
    # Store the existing API key before clearing
    existing_api_key = st.session_state.get("api_key", os.getenv("GROQ_API_KEY", ""))

    # Clear all existing session state keys
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    # Re-initialize all session state variables
    st.session_state.messages = []
    st.session_state.api_key = existing_api_key
    st.session_state.current_page = "Home"
    st.session_state.name_entered = False
    st.session_state.name = ""
    st.session_state.chat_manager = ChatManager()
    st.session_state.advice_generator = None
    st.session_state.initial_message_displayed = False


def navigate_to(page_name):
    st.session_state.current_page = page_name


# Page config
st.set_page_config(page_title="Career Advisor", layout="wide")

# Initialize session state if not already done
if "messages" not in st.session_state:
    reset_session_state()

# Sidebar
with st.sidebar:
    st.title("Career Advisor")
    api_key = st.text_input(
        "Groq API Key",
        value=st.session_state.api_key,
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

    if st.button("Clear Conversation", help="Clear the complete conversation"):
        reset_session_state()
        st.rerun()

    st.markdown("---")
    st.markdown("Contact us at: support@careerbot.ai")
    st.markdown(
        "Disclaimer: This chatbot provides general career\nadvice and does not guarantee job placements."
    )

if not st.session_state.api_key:
    st.warning("Please enter your Groq API Key in the sidebar to continue.")
    st.stop()

if st.session_state.current_page == "Home":
    st.title("Career Advisor ChatBot")
    st.markdown("##### From Curiosity to Career Clarity")

    if not st.session_state.get("name_entered", False):
        name = st.text_input(
            "Name:",
            placeholder="Enter your name",
            value=st.session_state.get("name", ""),
        )
        if name and name != st.session_state.get("name", ""):
            st.session_state.name = name
            st.session_state.name_entered = True

            if not st.session_state.initial_message_displayed:
                initial_message = f"""Hello {name}! I'm your AI Career Advisor. I can help you with:
                \n- Career guidance and planning
                \n- Skill development advice
                \n- Job search strategies
                \n- Industry insights
                \nWhat would you like to discuss about your career?"""

                if not any(
                    msg.get("role") == "assistant" and "Hello" in msg.get("content", "")
                    for msg in st.session_state.messages
                ):
                    st.session_state.messages.append(
                        {"role": "assistant", "content": initial_message}
                    )

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
    ## General Usage
    **How does the Career Advisor work?**  
    The Career Advisor uses advanced AI algorithms to provide tailored advice on career planning, skill development, job search strategies, and industry insights.

    **Do I need to create an account to use this tool?**  
    No, you do not need to create an account. Simply enter your name and start chatting.

    **Can I use the advisor without an API key?**  
    No, an API key is required to enable the AI functionality of the application.

    ---

    ## API Key
    **What is the Groq API Key, and why do I need it?**  
    The Groq API Key is used to authenticate and enable access to the AI capabilities of the Career Advisor.

    **Where can I obtain the API key?**  
    You can obtain the API key from your Groq account. Refer to the official Groq documentation for details.

    **Is my API key secure when entered into the application?**  
    Yes, the application does not share or store your API key beyond the current session.

    ---

    ## Functionality
    **What kind of career advice can I receive from the advisor?**  
    You can receive advice on career planning, skill development, job search strategies, certifications, and industry trends.

    **Can the advisor help with specific fields outside engineering?**  
    While the advisor specializes in engineering fields, some general advice may also be applicable to other domains.

    **How personalized is the advice provided?**  
    The advice is tailored based on the user input and conversation history to address your unique career needs.

    ---

    ## Technical Queries
    **What happens if I lose my internet connection while using the tool?**  
    The application requires an active internet connection. If the connection is lost, you may need to reload the page and re-enter your API key.

    **Can I save my conversation history for future reference?**  
    Currently, the tool does not support saving chat history. You can manually copy important advice if needed.

    **Is my data stored or shared?**  
    No, the application does not store or share your data. All interactions occur in real-time and are limited to your current session.

    ---

    ## Troubleshooting
    **Why am I not receiving any response after entering a prompt?**  
    Ensure that your API key is correct and your internet connection is stable. If the issue persists, try refreshing the page.

    **What should I do if the advisor gives incorrect or irrelevant advice?**  
    You can rephrase your question or provide more context to help the advisor give better advice.

    **How do I reset the application if it stops functioning?**  
    Use the "Clear Conversation" button in the sidebar to reset the application and start fresh.

    ---

    ## Features
    **Can I ask about skill development or certifications?**  
    Yes, the advisor can guide you on relevant skills and certifications based on your career goals.

    **Does the advisor provide job opportunities or industry contacts?**  
    No, the advisor does not provide job listings or industry contacts. It offers guidance to help you find opportunities.

    **How can I navigate between different sections like FAQs and Chat?**  
    Use the navigation buttons in the sidebar to switch between sections.

    ---

    ## Privacy and Security
    **Is my personal data (like name and questions) stored?**  
    No, the application does not store any personal data. All interactions are temporary and session-based.

    **How is my chat data used?**  
    Chat data is used solely to generate real-time responses and is not stored or shared.
    """)
