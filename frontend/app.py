import streamlit as st


# Function to navigate between pages
def navigate_to(page_name):
    st.session_state.current_page = page_name


# Initialize session state for current page
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

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
    if st.button("Career Resources"):
        navigate_to("Career Resources")
    if st.button("FAQs"):
        navigate_to("FAQs")

    st.markdown("---")

    st.markdown("Contact us at: support@careerbot.ai")
    st.markdown(
        "Disclaimer: This chatbot provides general career\nadvice and does not guarantee job placements."
    )


# Store the API Key
api_key = st.session_state.get("api_key", "")

name = st.text_input("Name:", placeholder="Enter your name")
print(name)

# Infinite Text Inputs Section (Main Body, Only Visible on Home Page)
if st.session_state.current_page == "Home":
    st.markdown("### Input Section:")
    if "inputs" not in st.session_state:
        st.session_state.inputs = [""]  # Initialize with one empty input field

    # Function to add a new input field
    def add_input():
        st.session_state.inputs.append("")  # Append a new empty input to the list

    # Render all current input fields
    for i, value in enumerate(st.session_state.inputs):
        st.session_state.inputs[i] = st.text_input(
            f"Input {i + 1}", value=value, key=f"input_{i}"
        )

    # Button to add a new input field dynamically
    if st.button("Add More Inputs"):
        add_input()
