from langchain_groq import ChatGroq


class Groq:
    def __init__(self, api_key: str):
        self.llm = ChatGroq(
            temperature=0, groq_api_key=api_key, model="llama-3.1-70b-versatile"
        )
