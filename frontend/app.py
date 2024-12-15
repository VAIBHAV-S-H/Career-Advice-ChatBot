import streamlit as st
import sys

sys.path.append("../")
from backend.advice_generator import AdviceGenerator
from backend.conversation_manager import ChatManager


# Function to navigate between pages
def navigate_to(page_name):
    st.session_state.current_page = page_name


# Initialize session state for current page
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "inputs" not in st.session_state:
    st.session_state.inputs = [""]  # Start with a single empty input field
if "responses" not in st.session_state:
    st.session_state.responses = [""]  # Initialize with a single empty response
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "name_entered" not in st.session_state:
    st.session_state.name_entered = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Track chat history for LLM response
if "welcome_message" not in st.session_state:
    st.session_state.welcome_message = ""  # Track the welcome message
if "input_count" not in st.session_state:
    st.session_state.input_count = 1  # Track the number of input fields
if "name" not in st.session_state:  # Track the user's name in session state
    st.session_state.name = ""

# Sidebar Content
with st.sidebar:
    st.text_input(
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
    if st.button("FAQs"):
        navigate_to("FAQs")

    st.markdown("---")

    st.markdown("Contact us at: support@careerbot.ai")
    st.markdown(
        "Disclaimer: This chatbot provides general career\nadvice and does not guarantee job placements."
    )

groq_api_key = st.session_state.api_key
if not groq_api_key:
    st.warning("Please enter your Groq API Key in the sidebar to continue.")
    st.stop()

advice_generator = AdviceGenerator(api_key=groq_api_key)
chat_manager = ChatManager()

# Main App Content
if st.session_state.current_page == "Home":
    st.title("Career Advice ChatBot")
    st.subheader("Your guide to building a brighter future")

    # Prompt for user's name
    if not st.session_state.name_entered:
        name = st.text_input(
            "Name:", placeholder="Enter your name", value=st.session_state.name
        )

        if name:
            st.session_state.name = name  # Save the name in session state
            st.session_state.name_entered = True
            chat_manager.user_history(f"My name is {name}")

            # Generate welcome message using LLM model
            welcome_message = f"""Hello {name}! I'm your AI Career Advisor. I can help you with:
            \n- Career guidance and planning
            \n- Skill development advice
            \n- Job search strategies
            \n- Industry insights

            \nWhat would you like to discuss about your career?"""
            chat_manager.bot_history(welcome_message)

            # Store the welcome message in session state
            st.session_state.welcome_message = welcome_message

    # Display the welcome message if not displayed already
    if st.session_state.name_entered and st.session_state.welcome_message:
        st.write(st.session_state.welcome_message)

    # Display Input Section after name is entered
    if st.session_state.name_entered:
        st.markdown("### Input Section:")

        # Function to add new input
        def add_new_input():
            st.session_state.input_count += 1
            st.session_state.inputs.append("")  # Add a new empty input field
            st.session_state.responses.append("")  # Add corresponding response entry

        # Display the existing input fields and responses
        for i in range(st.session_state.input_count):
            user_input = st.text_input(
                f"Input {i + 1}", value=st.session_state.inputs[i], key=f"input_{i}"
            )

            # If user provides input and presses Enter, generate advice
            if user_input:
                st.session_state.inputs[i] = user_input
                st.session_state.chat_history.append(f"You: {user_input}")

                # Store user input in chat history
                chat_manager.user_history(user_input)

                # Generate advice based on chat history
                history = chat_manager.get_history()
                advice = advice_generator.generate_advice(
                    history=history, user_input=user_input
                )

                # Store the AI response in session state and display
                st.session_state.responses[i] = (
                    advice  # Store the response for current input
                )
                st.session_state.chat_history.append(f"AI: {advice}")
                chat_manager.bot_history(advice)

            # Display responses below the input fields
            if st.session_state.responses[i]:
                st.write(f"**Career Coach:** {st.session_state.responses[i]}")

        # Store the current state of the button click in session state to avoid multiple triggers
        if "button_pressed" not in st.session_state:
            st.session_state.button_pressed = False

        # Button to add a new input field
        if st.button("Enter", key="add_input_button"):
            if not st.session_state.button_pressed:
                add_new_input()
                st.session_state.button_pressed = True  # Prevent double triggering

        # Reset the button state after the interaction
        if st.session_state.button_pressed:
            st.session_state.button_pressed = False

elif st.session_state.current_page == "FAQs":
    st.title("FAQs")
