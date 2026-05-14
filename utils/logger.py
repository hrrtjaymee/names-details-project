import logging
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), '../logs')
os.makedirs(LOG_DIR, exist_ok=True)

log_filename = os.path.join(LOG_DIR, f'pipeline_{datetime.now().strftime('%d%m%Y_%H%M%S')}.log')

def get_logger(name: str) -> logging.Logger:
    logger= logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    #terminal logger
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    #file logger
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger