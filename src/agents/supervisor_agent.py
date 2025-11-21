from src.agents.base_agent import BaseAgent
from src import tools
from src.tools.tool_manager import ToolManager
from src.memory.memory_manager import MemoryManager
from src.planning.react_planner import ReactPlanner
from src.config import config
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SupervisorAgent(BaseAgent):
    def __init__(self):
        self.tool_manager = ToolManager(tools)
        self.memory = MemoryManager()
        self.planner = ReactPlanner(self.tool_manager, self.memory)

    def run(self, user_query: str) -> str:
        logger.info(f"Starting new task with objective: {user_query}")
        self.memory.clear()
        
        for i in range(config.MAX_THOUGHTS):
            logger.info(f"--- Step {i+1}/{config.MAX_THOUGHTS} ---")
            
            observation, is_finished = self.planner.step(user_query)
            
            if is_finished:
                final_summary = f"Task completed successfully. Final summary: {observation}"
                logger.info(final_summary)
                return final_summary
        
        final_report = "Task stopped: Maximum number of thoughts reached."
        logger.warning(final_report)
        return final_report
