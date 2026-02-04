from app.config import load_config, ConfigError
from app.logger import setup_logger
from app.validator import DataValidator
from app.scheduler import AutomationScheduler

def run_pipeline():
    validator = DataValidator(CONFIG, LOGGER)
    validator.validate_all()

def main():
    global CONFIG, LOGGER

    LOGGER = setup_logger()

    try:
        CONFIG = load_config()
        LOGGER.info("Configuration loaded successfully")
    except ConfigError as e:
        LOGGER.error(f"Configuration error: {e}")
        return
    except Exception:
        LOGGER.exception("Unexpected startup failure")
        return

    scheduler = AutomationScheduler(
        interval_minutes=CONFIG["schedule_interval_minutes"],
        job=run_pipeline,
        logger=LOGGER
    )

    scheduler.start()

if __name__ == "__main__":
    main()
