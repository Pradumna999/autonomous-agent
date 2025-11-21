from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from src.tools.base_tool import BaseTool
from src.utils.logger import get_logger
import os
import time

logger = get_logger(__name__)

class BrowserAutomationTool(BaseTool):
    def __init__(self):
        self.driver = None

    @property
    def name(self) -> str:
        return "browser_automation"

    @property
    def description(self) -> str:
        return (
            "Performs web browser automation tasks. "
            "Args: operation (str), **kwargs. "
            "Valid operations: 'open_url', 'find_element', 'click_element', 'type_in_element', 'get_page_source', 'screenshot', 'close_browser', 'fill_form', 'get_element_text', 'wait_for_element'. "
            "For 'open_url', provide 'url'. "
            "For 'find_element', provide 'selector'. "
            "For 'click_element', provide 'selector'. "
            "For 'type_in_element', provide 'selector' and 'text'. "
            "For 'screenshot', provide 'file_path'."
            "For 'fill_form', provide 'form_data' (a dictionary of selectors and values)."
            "For 'get_element_text', provide 'selector'."
            "For 'wait_for_element', provide 'selector' and 'timeout' (optional, default 10)."
        )

    def _initialize_driver(self):
        if self.driver is None:
            try:
                options = webdriver.ChromeOptions()
                options.add_argument("--headless")
                self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
                logger.info("Chrome driver initialized.")
            except Exception as e:
                logger.error(f"Failed to initialize Chrome driver: {e}")
                raise

    def execute(self, operation: str, **kwargs) -> str:
        logger.info(f"Executing browser automation operation '{operation}' with args {kwargs}")
        try:
            self._initialize_driver()

            if operation == "open_url":
                url = kwargs.get("url")
                if not url:
                    return "Error: 'url' is required for 'open_url'."
                self.driver.get(url)
                return f"Successfully opened URL: {url}"

            elif operation == "find_element":
                selector = kwargs.get("selector")
                if not selector:
                    return "Error: 'selector' is required for 'find_element'."
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                return str(element.get_attribute('outerHTML'))

            elif operation == "click_element":
                selector = kwargs.get("selector")
                if not selector:
                    return "Error: 'selector' is required for 'click_element'."
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                element.click()
                return f"Successfully clicked element with selector '{selector}'."

            elif operation == "type_in_element":
                selector = kwargs.get("selector")
                text = kwargs.get("text")
                if not selector or text is None:
                    return "Error: 'selector' and 'text' are required for 'type_in_element'."
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                element.send_keys(text)
                return f"Successfully typed '{text}' in element with selector '{selector}'."

            elif operation == "get_page_source":
                return self.driver.page_source

            elif operation == "fill_form":
                form_data = kwargs.get("form_data")
                if not isinstance(form_data, dict):
                    return "Error: 'form_data' must be a dictionary of selectors and values."
                for selector, value in form_data.items():
                    try:
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        element.send_keys(value)
                    except Exception as e:
                        return f"Error filling form for selector '{selector}': {e}"
                return "Successfully filled the form."

            elif operation == "get_element_text":
                selector = kwargs.get("selector")
                if not selector:
                    return "Error: 'selector' is required for 'get_element_text'."
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                return element.text

            elif operation == "wait_for_element":
                selector = kwargs.get("selector")
                timeout = kwargs.get("timeout", 10)
                if not selector:
                    return "Error: 'selector' is required for 'wait_for_element'."
                wait = WebDriverWait(self.driver, timeout)
                element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                return f"Element with selector '{selector}' is present."

            elif operation == "screenshot":
                file_path = kwargs.get("file_path")
                if not file_path:
                    return "Error: 'file_path' is required for 'screenshot'."
                self.driver.save_screenshot(file_path)
                return f"Screenshot saved to {file_path}"

            elif operation == "close_browser":
                if self.driver:
                    self.driver.quit()
                    self.driver = None
                    return "Browser closed."
                return "Browser not open."

            else:
                return f"Error: Unknown browser automation operation '{operation}'."

        except Exception as e:
            logger.error(f"Browser automation tool error: {e}")
            return f"Error during browser automation: {e}"
