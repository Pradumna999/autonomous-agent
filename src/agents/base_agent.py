from abc import ABC, abstractmethod

class BaseAgent(ABC):
    @abstractmethod
    def run(self, user_query: str) -> str:
        pass
