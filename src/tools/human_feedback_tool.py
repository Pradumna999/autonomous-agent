from src.tools.base_tool import BaseTool
from src.utils.logger import get_logger

logger = get_logger(__name__)

class HumanFeedbackTool(BaseTool):
    @property
    def name(self) -> str:
        return "human_feedback"

    @property
    def description(self) -> str:
        return (
            "Asks the human user for input or clarification. "
            "Use this when you are stuck or need more information. "
            "Args: question (str)."
        )

    def execute(self, question: str) -> str:
        logger.info(f"Asking user for feedback: '{question}'")
        
        print(f"\n--- AGENT REQUEST ---")
        print(f"The agent is asking for your help: {question}")
        answer = input("Your response: ")
        
        logger.info(f"User responded: '{answer}'")
        return f"The user responded: '{answer}'"
