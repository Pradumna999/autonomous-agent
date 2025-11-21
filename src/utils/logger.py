import logging
import colorama
from src.config import config

colorama.init()

class ColorFormatter(logging.Formatter):
    LOG_COLORS = {
        logging.DEBUG: colorama.Fore.CYAN,
        logging.INFO: colorama.Fore.GREEN,
        logging.WARNING: colorama.Fore.YELLOW,
        logging.ERROR: colorama.Fore.RED,
        logging.CRITICAL: colorama.Fore.MAGENTA,
    }

    def format(self, record):
        color = self.LOG_COLORS.get(record.levelno)
        message = super().format(record)
        if color:
            message = color + message + colorama.Style.RESET_ALL
        return message

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    
    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = ColorFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
