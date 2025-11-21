import subprocess
from src.tools.base_tool import BaseTool
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SystemCommandTool(BaseTool):
    @property
    def name(self) -> str:
        return "system_command"

    @property
    def description(self) -> str:
        return (
            "Executes a command in the Windows shell. "
            "Args: command (str). "
            "Returns the standard output and standard error."
        )

    def execute(self, command: str) -> str:
        logger.info(f"Executing system command: '{command}'")
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                check=False,
                encoding='utf-8'
            )
            
            output = ""
            if result.stdout:
                output += f"STDOUT:\n{result.stdout}\n"
            if result.stderr:
                output += f"STDERR:\n{result.stderr}\n"
            
            if not output:
                return "Command executed with no output."
                
            return output

        except Exception as e:
            logger.error(f"System command tool error: {e}")
            return f"Error executing command '{command}': {e}"
