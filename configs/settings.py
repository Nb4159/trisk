"""import os

class Settings:
    PROJECT_NAME = "risk-engine"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

settings = Settings()"""
import yaml


def load_config(config_path: str):

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    return config