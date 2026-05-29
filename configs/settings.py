import os

class Settings:
    PROJECT_NAME = "risk-engine"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

settings = Settings()
