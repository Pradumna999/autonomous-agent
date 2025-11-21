from typing import List, Dict, Any
from ..utils.logger import get_logger

logger = get_logger(__name__)

class MemoryManager:
    def __init__(self):
        self.history: List[Dict[str, Any]] = []

    def add_entry(self, entry_type: str, content: str):
        entry = {"type": entry_type, "content": content}
        self.history.append(entry)
        logger.debug(f"Added to memory: {entry}")

    def get_full_history(self) -> str:
        formatted_history = ""
        for entry in self.history:
            formatted_history += f"{entry['type'].upper()}: {entry['content']}\n"
        return formatted_history

    def clear(self):
        self.history = []
        logger.info("Memory cleared.")
