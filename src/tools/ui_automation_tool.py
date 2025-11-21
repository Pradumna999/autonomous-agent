from pywinauto.application import Application
from pywinauto import Desktop
from src.tools.base_tool import BaseTool
from src.utils.logger import get_logger

logger = get_logger(__name__)

class UIAutomationTool(BaseTool):
    @property
    def name(self) -> str:
        return "ui_automation"

    @property
    def description(self) -> str:
        return (
            "Performs UI automation tasks. "
            "Args: operation (str), **kwargs. "
            "Valid operations: 'list_windows', 'get_controls', 'click_control'. "
            "For 'get_controls', provide 'window_title'. "
            "For 'click_control', provide 'window_title' and 'control_specifier'."
        )

    def execute(self, operation: str, **kwargs) -> str:
        logger.info(f"Executing UI automation operation '{operation}' with args {kwargs}")
        try:
            if operation == "list_windows":
                windows = Desktop(backend="uia").windows()
                return "\n".join([w.window_text() for w in windows])
            
            elif operation == "get_controls":
                window_title = kwargs.get("window_title")
                if not window_title:
                    return "Error: 'window_title' is required for 'get_controls'."
                
                app = Application(backend="uia").connect(title_re=f".*{window_title}.*", timeout=10)
                
                windows = app.windows(title_re=f".*{window_title}.*")
                if not windows:
                    return f"Error: No window with title matching '{window_title}' found."
                
                main_window = None
                for w in windows:
                    if w.is_active():
                        main_window = w
                        break
                if not main_window:
                    main_window = windows[0]

                logger.info(f"Found window: {main_window.window_text()}")
                controls = main_window.descendants()
                return "\n".join([str(c.element_info) for c in controls])

            elif operation == "click_control":
                window_title = kwargs.get("window_title")
                control_specifier = kwargs.get("control_specifier")
                if not window_title or not control_specifier:
                    return "Error: 'window_title' and 'control_specifier' are required."

                app = Application(backend="uia").connect(title_re=f".*{window_title}.*", timeout=10)

                windows = app.windows(title_re=f".*{window_title}.*")
                if not windows:
                    return f"Error: No window with title matching '{window_title}' found."

                main_window = None
                for w in windows:
                    if w.is_active():
                        main_window = w
                        break
                if not main_window:
                    main_window = windows[0]
                
                logger.info(f"Targeting window: {main_window.window_text()}")
                control = main_window.child_window(best_match=control_specifier)
                control.click_input()
                return f"Successfully clicked control '{control_specifier}' in window '{window_title}'."

            else:
                return f"Error: Unknown UI automation operation '{operation}'."

        except Exception as e:
            logger.error(f"UI automation tool error: {e}")
            return f"Error during UI automation: {e}"
