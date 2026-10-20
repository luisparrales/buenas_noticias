import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def env_int(name, default):
    try:
        return int(os.getenv(name, default))
    except (TypeError, ValueError):
        return default


class Config:
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    USERS_CSV = os.getenv("USERS_CSV", str(BASE_DIR / "data" / "users.csv"))
    PREFERENCES_CSV = os.getenv("PREFERENCES_CSV", str(BASE_DIR / "data" / "preferences.csv"))

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GNEWS_API_KEY = os.getenv("GNEWS_API_KEY", "")
    NEWS_LANGUAGE = os.getenv("NEWS_LANGUAGE", "es")
    NEWS_COUNTRY = os.getenv("NEWS_COUNTRY", "mx")
    NEWS_MAX_RESULTS = max(1, min(env_int("NEWS_MAX_RESULTS", 10), 10))

    SMTP_HOST = os.getenv("SMTP_HOST", "")
    SMTP_PORT = env_int("SMTP_PORT", 587)
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", "")
    SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "Buenos Días, Buenas Noticias")
    SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
