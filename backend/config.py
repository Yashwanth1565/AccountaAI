"""
==========================================================
AccountaAI
Configuration File
----------------------------------------------------------
Loads environment variables and project-wide settings.
==========================================================
"""

from pathlib import Path
import os

from dotenv import load_dotenv

# ---------------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------------

load_dotenv()

# ---------------------------------------------------------
# Project Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"

TRANSCRIPT_DIR = BASE_DIR / "transcripts"

CHROMA_DB_DIR = BASE_DIR / "chroma_db"

DATABASE_PATH = BASE_DIR / "accountaai.db"

LOG_DIR = BASE_DIR / "logs"

# ---------------------------------------------------------
# Create folders automatically
# ---------------------------------------------------------

UPLOAD_DIR.mkdir(exist_ok=True)

TRANSCRIPT_DIR.mkdir(exist_ok=True)

CHROMA_DB_DIR.mkdir(exist_ok=True)

LOG_DIR.mkdir(exist_ok=True)

VIDEO_EXTENSIONS = (
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".webm"
)

AUDIO_EXTENSIONS = [
    ".mp3",
    ".wav",
    ".m4a"
]
# ---------------------------------------------------------
# Gemini
# ---------------------------------------------------------

GOOGLE_API_KEY = (
    os.getenv("GOOGLE_API_KEY")
    or os.getenv("GEMINI_API_KEY")
)

GEMINI_MODEL = "gemini-2.5-flash"

# ---------------------------------------------------------
# Whisper
# ---------------------------------------------------------

WHISPER_MODEL = "base"

# ---------------------------------------------------------
# Embedding Model
# ---------------------------------------------------------

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

# ---------------------------------------------------------
# Chroma
# ---------------------------------------------------------

CHROMA_COLLECTION = "meeting_memory"

# ---------------------------------------------------------
# Langfuse
# ---------------------------------------------------------

LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")

LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")

LANGFUSE_HOST = os.getenv(
    "LANGFUSE_HOST",
    "https://cloud.langfuse.com"
)

# ---------------------------------------------------------
# Email (Resend)
# ---------------------------------------------------------

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

# ---------------------------------------------------------
# Scheduler
# ---------------------------------------------------------

CHECK_INTERVAL_MINUTES = 1

# ---------------------------------------------------------
# App
# ---------------------------------------------------------

APP_NAME = "AccountaAI"

APP_VERSION = "1.0.0"

DEBUG = True
