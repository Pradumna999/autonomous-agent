import google.generativeai as genai
from src.config import config
from src.utils.logger import get_logger

logger = get_logger(__name__)

class LLMProvider:
    def __init__(self):
        if not config.GEMINI_API_KEY:
            raise ValueError("Gemini API key is not configured.")
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(config.LLM_MODEL)

    def get_completion(self, prompt: str, temperature: float = 0.1) -> str:
        try:
            logger.debug(f"Sending prompt to Gemini: {prompt[:200]}...")
            generation_config = genai.types.GenerationConfig(
                temperature=temperature
            )
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            content = response.text
            logger.debug(f"Received response from Gemini: {content[:200]}...")
            return content.strip()
        except Exception as e:
            logger.error(f"An unexpected error occurred while calling Gemini: {e}")
            if "API key not valid" in str(e):
                 raise ValueError("The provided Gemini API key is not valid. Please check your .env file.")
            raise

llm_provider = LLMProvider()
