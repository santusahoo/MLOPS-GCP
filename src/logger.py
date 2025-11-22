import logging
import os
from datetime import datetime

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
LOG_FILE_NAME = os.path.join(LOGS_DIR, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_NAME,
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

def get_logger(name):
    """Function to get a logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger