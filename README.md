# Career Advisor Application

This application is a Streamlit-based AI-powered career advisor specialized in engineering fields. It provides tailored career guidance, skill development advice, job search strategies, and industry insights to help users achieve their career goals.

The app is also deployed in streamlit

Visit link : [ChatBotApp](https://growcareer.streamlit.app)
---

## Features

- **Personalized Career Advice:** Tailored guidance based on user input and conversation history.
- **Empathetic and Actionable Responses:** Motivational and practical steps for career improvement.
- **AI-Powered Chat Interface:** Real-time responses using the Groq API.
- **FAQs Section:** Quick answers to common questions about the tool and its usage.
- **Session-Based Conversations:** Secure and private interactions with no data storage.

---

## Prerequisites

1. **Python:** Make sure Python 3.8 or higher is installed on your system.
2. **Groq API Key:** Obtain your API key from the Groq platform to enable AI functionality.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/RishabhJeppu/Career-Advice-ChatBot.git
cd Career-Advice-ChatBot
```

### 2. Set Up Virtual Environment

Create and activate a virtual environment for the project:

#### On Windows:

```bash
venv\Scripts\activate
```

#### On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

Use the `requirements.txt` file to install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

To launch the Career Advisor application, run the following command:

```bash
streamlit run app.py
```

This will open the application in your default web browser. If it doesn’t open automatically, navigate to the URL shown in the terminal (typically `http://localhost:8501`).

---

## Usage

1. **Enter Groq API Key:** Provide your API key in the sidebar.
2. **Start Chatting:** Enter your name and type career-related questions to receive advice.
3. **Navigate:** Use the sidebar to switch between the chat interface and the FAQs section.
4. **Reset Conversation:** Clear all session data using the "Clear Conversation" button.

---

## FAQs

- **What is the Groq API Key?**

  - It is a key used to authenticate and enable AI-powered features. Obtain it from the Groq platform.

- **Can I use this app without an API key?**

  - No, the Groq API key is mandatory to use the app.
  - To manage your keys, visit the [Groq Console Keys](https://console.groq.com/keys)

- **Is my data secure?**

  - Yes, the application does not store or share any personal data. All interactions are session-based.

---

## Troubleshooting

- **Issue:** No response after entering a prompt.

  - **Solution:** Verify your API key and ensure a stable internet connection.

- **Issue:** Application stops responding.

  - **Solution:** Use the "Clear Conversation" button in the sidebar to reset the app.


