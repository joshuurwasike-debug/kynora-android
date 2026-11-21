import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"


def load_environment():
    if not ENV_FILE.exists():
        return

    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_environment()


class Settings:
    APP_NAME = os.getenv("APP_NAME", "KYNORA")
    APP_ENV = os.getenv("APP_ENV", "development")
    SECRET_KEY = os.getenv("SECRET_KEY", "")
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./data/kynora.db"
    )
    DATABASE_PATH = BASE_DIR / "data" / "kynora.db"


settings = Settings()
