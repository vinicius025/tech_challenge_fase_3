from loguru import logger
from .config import settings
import sys

def setup_logging():
    logger.remove()
    logger.add(sys.stdout, level="INFO")
    logger.add(settings.LOG_PATH, level="INFO", rotation="5 MB", retention="10 days", enqueue=True)
    return logger
