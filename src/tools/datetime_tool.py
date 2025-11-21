import datetime
from src.tools.base_tool import BaseTool
from src.utils.logger import get_logger

logger = get_logger(__name__)

class DateTimeTool(BaseTool):
    @property
    def name(self) -> str:
        return "get_datetime"

    @property
    def description(self) -> str:
        return "Returns the current date and time."

    def execute(self) -> str:
        logger.info("Getting current date and time")
        try:
            return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            logger.error(f"DateTime tool error: {e}")
            return f"Error getting date and time: {e}"
