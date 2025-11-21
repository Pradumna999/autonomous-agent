import json
import re
from src.tools.tool_manager import ToolManager
from src.memory.memory_manager import MemoryManager
from src.utils.llm_provider import llm_provider
from src.utils.logger import get_logger

logger = get_logger(__name__)

class ReactPlanner:
    def __init__(self, tool_manager: ToolManager, memory_manager: MemoryManager):
        self.tool_manager = tool_manager
        self.memory = memory_manager
        self.llm = llm_provider

    def _build_prompt(self, objective: str) -> str:
        return f"""
**System Persona:**
You are a highly intelligent and autonomous AI agent designed to operate on a Windows desktop. Your primary goal is to achieve the user's objective by breaking it down into logical steps and using the available tools. You are methodical, careful, and always reflect on the outcome of your actions.

**Objective:**
{objective}

**Instructions:**
You must operate in a cycle of Thought, Action, Observation.
1.  **Thought**: Analyze the current situation, including the history of actions and observations. Formulate a clear, concise plan for your next immediate action. Think step-by-step.
2.  **Action**: Based on your thought, select the single most appropriate tool to execute next. Format your action as a single JSON object.
3.  **Observation**: After you provide an action, the system will execute it and you will receive an observation of the result.

**Error Handling and Self-Correction:**
If an Observation indicates an error or that the previous action failed, you MUST address it.
-   **Analyze the Error**: In your next Thought, identify the cause of the error.
-   **Change the Plan**: Do not repeat the failed action. Formulate a new plan to either fix the issue or try a different approach.
-   **Use Tools to Investigate**: Use tools like `file_system` to check if a file was created, or `human_feedback` to ask for help if you are stuck.
-   **Your primary goal is to recover from failures and find a successful path.**

**Pro-Tip for Web Tasks:**
For tasks involving websites, it is much more efficient to open the browser directly to the target URL. For example, instead of just opening Firefox, use the `system_command` tool to run `start firefox "https://www.youtube.com"`.

**Available Tools:**
{self.tool_manager.tool_prompt}

**Action JSON Format:**
Your response must contain exactly one JSON block formatted like this:
```json
{{
  "thought": "Your reasoning and plan for the next action.",
  "action": {{
    "tool": "tool_name",
    "args": {{
      "arg_name1": "value1",
      "arg_name2": "value2"
    }}
  }}
}}
```

**Completion:**
Once you are certain the objective has been fully achieved, use the "finish" tool.
```json
{{
  "thought": "I have successfully completed the objective.",
  "action": {{
    "tool": "finish",
    "args": {{
      "summary": "A detailed summary of what was accomplished and the final result."
    }}
  }}
}}
```

**Task History (Thought, Action, Observation):**
{self.memory.get_full_history()}
Your turn. Provide your next thought and action in the specified JSON format.
"""

    def _parse_llm_response(self, response: str) -> tuple[str, dict | None]:
        match = re.search(r"```json\n(.*?)\n```", response, re.DOTALL)
        if not match:
            logger.warning("Could not find a JSON block in the LLM response.")
            return "Error: No JSON action block found.", None

        try:
            parsed_json = json.loads(match.group(1).strip())
            thought = parsed_json.get("thought", "")
            action = parsed_json.get("action")
            return thought, action
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode action JSON: {e}")
            return f"Error: Invalid JSON format. {e}", None
        except Exception as e:
            logger.error(f"An unexpected error occurred during parsing: {e}")
            return f"Error parsing response: {e}", None

    def step(self, objective: str) -> tuple[str, bool]:
        prompt = self._build_prompt(objective)
        response = self.llm.get_completion(prompt)
        
        thought, action_data = self._parse_llm_response(response)
        
        if not thought or not action_data:
            observation = "Error: Could not parse thought or action from response. Please check the format."
            self.memory.add_entry("observation", observation)
            logger.error(observation)
            return observation, False

        self.memory.add_entry("thought", thought)
        logger.info(f"Thought: {thought}")

        if "tool" not in action_data:
            return "Error: 'tool' key missing from action data.", False

        tool_name = action_data["tool"]
        tool_args = action_data.get("args", {})
        
        self.memory.add_entry("action", json.dumps(action_data))
        logger.info(f"Action: {tool_name}({tool_args})")

        if tool_name == "finish":
            summary = tool_args.get("summary", "Objective completed.")
            return summary, True

        tool = self.tool_manager.get_tool(tool_name)
        if not tool:
            observation = f"Error: Tool '{tool_name}' not found."
        else:
            try:
                observation = tool.execute(**tool_args)
            except Exception as e:
                observation = f"Error executing tool '{tool_name}': {e}"
        
        self.memory.add_entry("observation", str(observation))
        logger.info(f"Observation: {str(observation)[:300]}...")

        return str(observation), False
