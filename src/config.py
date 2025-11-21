import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    LLM_MODEL = "gemini-2.5-pro"

    MAX_THOUGHTS = 100

    LOG_LEVEL = "INFO"

config = Config()

if not config.GEMINI_API_KEY:
    raise ValueError(
        "Gemini API key is not set. Please ensure a .env file exists "
        "with your GEMINI_API_KEY."
    )
