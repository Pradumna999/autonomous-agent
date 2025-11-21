import os
from src.tools.base_tool import BaseTool
from src.utils.logger import get_logger

logger = get_logger(__name__)

class FileSystemTool(BaseTool):
    @property
    def name(self) -> str:
        return "file_system"

    @property
    def description(self) -> str:
        return (
            "Performs file system operations. "
            "Args: operation (str), path (str), content (str, optional). "
            "Valid operations: 'read', 'write', 'list', 'delete'."
        )

    def execute(self, operation: str, path: str, content: str = None) -> str:
        logger.info(f"Executing file system operation '{operation}' on path '{path}'")
        try:
            if operation == "read":
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
            elif operation == "write":
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                return f"Successfully wrote to file: {path}"
            elif operation == "list":
                return "\n".join(os.listdir(path))
            elif operation == "delete":
                os.remove(path)
                return f"Successfully deleted file: {path}"
            else:
                return f"Error: Unknown file system operation '{operation}'."
        except FileNotFoundError:
            return f"Error: Path not found: {path}"
        except Exception as e:
            logger.error(f"File system tool error: {e}")
            return f"Error during file system operation: {e}"
