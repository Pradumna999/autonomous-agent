import inspect
import pkgutil
from src.tools.base_tool import BaseTool
from src.utils.logger import get_logger

logger = get_logger(__name__)

class ToolManager:
    def __init__(self, tool_package):
        self.tools = self._discover_tools(tool_package)
        self.tool_prompt = self._build_tool_prompt()

    def _discover_tools(self, package) -> dict[str, BaseTool]:
        tools = {}
        logger.info(f"Discovering tools in package: {package.__name__}")
        for _, name, _ in pkgutil.iter_modules(package.__path__):
            try:
                module = __import__(f"{package.__name__}.{name}", fromlist=["*"])
                for member_name, member_obj in inspect.getmembers(module):
                    if (
                        inspect.isclass(member_obj)
                        and issubclass(member_obj, BaseTool)
                        and member_obj is not BaseTool
                    ):
                        instance = member_obj()
                        tools[instance.name] = instance
                        logger.info(f"Successfully loaded tool: {instance.name}")
            except ImportError as e:
                logger.warning(f"Could not load tool from module '{name}' due to missing dependency: {e}")
                logger.warning("Please install the required packages to enable this tool.")
        return tools

    def _build_tool_prompt(self) -> str:
        prompt = "You have access to the following tools:\n"
        for name, tool in self.tools.items():
            prompt += f"- {name}: {tool.description}\n"
        return prompt

    def get_tool(self, name: str) -> BaseTool | None:
        return self.tools.get(name)
