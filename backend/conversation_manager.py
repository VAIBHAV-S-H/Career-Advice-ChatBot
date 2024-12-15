class ChatManager:
    def __init__(self):
        self.history = []

    def get_history(self):
        return "\n".join(self.history)

    def bot_history(self, advice: str):
        self.history.append(f"Bot: {advice}")

    def user_history(self, query: str):
        self.history.append(f"User: {query}")
