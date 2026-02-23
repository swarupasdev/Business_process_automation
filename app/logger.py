import logging
from logging.handlers import RotatingFileHandler
import os
import json
from datetime import datetime
from app.paths import BASE_DIR


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record)


def setup_logger():
    logs_dir = os.path.join(BASE_DIR, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    log_file = os.path.join(logs_dir, "app.log")

    logger = logging.getLogger("automation")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    handler = RotatingFileHandler(
        log_file,
        maxBytes=1_000_000,
        backupCount=5
    )

    handler.setFormatter(JsonFormatter())

    logger.addHandler(handler)
    return logger