import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"
DATA_DIR = BASE_DIR / "data"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# Database file path
DB_PATH = DATA_DIR / "profile.db"

# Server configuration
SECRET_KEY = os.getenv("SECRET_KEY", "dev-profile-key-siddharth-2026")
DEBUG = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 5000))

# Admin Credentials
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "siddharth2026")
TOKEN_MAX_AGE = int(os.getenv("TOKEN_MAX_AGE", 86400))  # 24 hours in seconds

# CORS settings
CORS_ORIGINS = ["*", "http://localhost:5000", "http://127.0.0.1:5000"]
