# Python
import os

DEBUG = os.environ["DEBUG"]
SECRET_KEY = os.environ["SECRET_KEY"]

# Database configuration
USE_DATABASE = os.environ["USE_DATABASE"]

DATABASE = (
    {
        "ENGINE": "postgresql",  # postgresql or sqlite
        "NAME": os.environ["DATABASE_NAME"],
        # Only for postgresql database
        "USER": os.environ["DATABASE_USER"],
        "PASSWORD": os.environ["DATABASE_PASSWORD"],
        "HOST": os.environ["DATABASE_HOST"],
        "PORT": os.environ["DATABASE_PORT"],
    }
    if USE_DATABASE.lower() == "true"
    else {}
)

# Twilio config
TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]

# OpenIA config
OPENIA_API_KEY = os.environ["OPENIA_API_KEY"]
OPENIA_API_ENDPOINT = "https://api.openai.com/v1/chat/completions"

# Cors
origins = os.getenv("ALLOWER_CORS_ORIGINS", "")
ALLOWER_CORS_ORIGINS = [origin.strip() for origin in origins.split(",") if origin]
