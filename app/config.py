import yaml
import os

class ConfigError(Exception):
    pass

def load_config(path="config.yaml"):
    if not os.path.exists(path):
        raise ConfigError(f"Config file not found: {path}")

    with open(path, "r") as f:
        config = yaml.safe_load(f)

    required_keys = [
        "input_format",
        "input_path",
        "output_path",
        "failed_path",
        "required_columns",
        "schedule_interval_minutes",
    ]

    for key in required_keys:
        if key not in config:
            raise ConfigError(f"Missing config key: {key}")

    return config
