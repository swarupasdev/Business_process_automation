import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger():
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("automation")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=1_000_000,
        backupCount=5
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
