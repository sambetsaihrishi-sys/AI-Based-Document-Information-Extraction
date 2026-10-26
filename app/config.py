import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


APP_NAME = os.getenv(
    "APP_NAME",
    "AI-Based Document Information Extraction"
)

MAX_FILE_SIZE_MB = int(
    os.getenv("MAX_FILE_SIZE_MB", "5")
)

MAX_PDF_PAGES = int(
    os.getenv("MAX_PDF_PAGES", "5")
)

TESSERACT_CMD = os.getenv(
    "TESSERACT_CMD",
    "tesseract"
)

MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024