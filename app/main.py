from app.config import load_config, ConfigError
from app.logger import setup_logger

def main():
    logger = setup_logger()

    try:
        config = load_config()
        logger.info("Configuration loaded successfully")
        logger.info(f"Running with config: {config}")
    except ConfigError as e:
        logger.error(f"Configuration error: {e}")
        return
    except Exception as e:
        logger.exception("Unexpected startup failure")
        return

    logger.info("Automation system initialized")

if __name__ == "__main__":
    main()
