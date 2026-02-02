from app.config import load_config, ConfigError
from app.logger import setup_logger
from app.validator import DataValidator

def main():
    logger = setup_logger()

    try:
        config = load_config()
        logger.info("Configuration loaded successfully")
    except ConfigError as e:
        logger.error(f"Configuration error: {e}")
        return
    except Exception:
        logger.exception("Unexpected startup failure")
        return

    validator = DataValidator(config, logger)
    validator.validate_all()

    logger.info("Validation phase completed")

if __name__ == "__main__":
    main()
