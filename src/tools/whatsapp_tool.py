import pywhatkit
from src.tools.base_tool import BaseTool
from src.utils.logger import get_logger

logger = get_logger(__name__)

class WhatsAppTool(BaseTool):
    @property
    def name(self) -> str:
        return "send_whatsapp_message"

    @property
    def description(self) -> str:
        return (
            "Sends a WhatsApp message to a given phone number. "
            "Args: phone_no (str), message (str), hour (int), minute (int). "
            "The phone number must be a string with the country code."
        )

    def execute(self, phone_no: str, message: str, hour: int, minute: int) -> str:
        logger.info(f"Sending WhatsApp message to {phone_no}")
        try:
            pywhatkit.sendwhatmsg(phone_no, message, hour, minute)
            return f"WhatsApp message scheduled to be sent to {phone_no} at {hour}:{minute}."
        except Exception as e:
            logger.error(f"WhatsApp tool error: {e}")
            return f"Error sending WhatsApp message: {e}"
