class ChatManager:
    def __init__(self):
        self.history = []
        self.max_history = 5  # Maximum number of conversation pairs to keep

    def get_history(self):
        # Format the history as a structured conversation
        formatted_history = []
        for i in range(0, len(self.history), 2):
            if i + 1 < len(self.history):
                formatted_history.append(
                    f"User: {self.history[i]}\nAssistant: {self.history[i+1]}"
                )
        return "\n\n".join(formatted_history[-self.max_history :])

    def bot_history(self, advice: str):
        self.history.append(advice)
        # Trim history if it gets too long
        if len(self.history) > self.max_history * 2:
            self.history = self.history[-(self.max_history * 2) :]

    def user_history(self, query: str):
        self.history.append(query)
        # Trim history if it gets too long
        if len(self.history) > self.max_history * 2:
            self.history = self.history[-(self.max_history * 2) :]

    def clear_history(self):
        self.history = []
