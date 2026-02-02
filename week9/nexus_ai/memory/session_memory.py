from typing import List, Dict

class SessionMemory:
    """Short-term memory (conversation buffer)"""

    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        self.history: List[Dict[str, str]] = []

    def add(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.max_turns:
            self.history.pop(0)

    def get_context(self) -> str:
        return "\n".join([f"{m['role']}: {m['content']}" for m in self.history])

    def clear(self):
        self.history = []