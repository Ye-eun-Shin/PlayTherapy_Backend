import os


class Settings:
    VERSION = "0.0.22"
    APP_TITLE = "Contents"
    PROJECT_NAME = "Play Therapy"

    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    BASE_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))


settings = Settings()
