# -*- coding: utf-8 -*-
"""
config.py
=========
Central configuration for the Arabic Meeting Summarizer project.

Edit the plain values below (YOUTUBE_URL, USE_FAST_MODE, ...) to change
pipeline behaviour. API keys are NOT hard-coded here — they are read from
environment variables (or a local `.env` file) so you never commit secrets
to version control. See README.md -> "Setting your API keys".
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load variables from a local .env file, if one exists, into os.environ.
# This lets you keep API keys in a file that is git-ignored instead of
# typing `set MISTRAL_API_KEY=...` every time you open a new terminal.
load_dotenv()

# ──────────────────────────────────────────────────────────────────────────
# 1) MEETING SOURCE
# ──────────────────────────────────────────────────────────────────────────
# The YouTube URL of the meeting/recording to summarize.
# You can override this on the command line, e.g.:
#   python src/main.py --url "https://www.youtube.com/watch?v=XXXX"
YOUTUBE_URL: str = "https://www.youtube.com/watch?v=oueP7_CBIoo"

# ──────────────────────────────────────────────────────────────────────────
# 2) PERFORMANCE / QUALITY TRADE-OFFS
# ──────────────────────────────────────────────────────────────────────────
USE_FAST_MODE: bool = True        # True = faster ASR (smaller beam size)
NUM_SPEAKERS_HINT = None          # None = auto-detect, or an int like 2 or 3

# ──────────────────────────────────────────────────────────────────────────
# 3) MODELS
# ──────────────────────────────────────────────────────────────────────────
# Arabic-specialised chat model, served via Mistral's official API
# (OpenAI-compatible endpoint).
ARABIC_MODEL_BASE_URL: str = "https://api.mistral.ai/v1"
ARABIC_MODEL_ID: str = "mistral-saba-latest"  # check console.mistral.ai for the current name

# Google Gemini model used to build the final structured report.
GEMINI_MODEL_ID: str = "gemini-2.5-flash"

# Faster-Whisper ASR model size. "large-v3-turbo" needs a decent GPU for
# good speed; use "small" or "medium" on CPU-only machines if it is too slow.
WHISPER_MODEL_SIZE: str = "large-v3-turbo"

# ──────────────────────────────────────────────────────────────────────────
# 4) API KEYS  (never hard-code real keys here — use environment variables)
# ──────────────────────────────────────────────────────────────────────────
ARABIC_MODEL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "")
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

# ──────────────────────────────────────────────────────────────────────────
# 5) PATHS  (all relative to this file so the project works from any drive)
# ──────────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent

DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "meeting_output"
MODELS_DIR = BASE_DIR / "models"
VECTORSTORE_DIR = BASE_DIR / "data" / "vectorstore"

for _dir in (DATA_RAW_DIR, DATA_PROCESSED_DIR, OUTPUT_DIR, MODELS_DIR, VECTORSTORE_DIR):
    _dir.mkdir(parents=True, exist_ok=True)

# ──────────────────────────────────────────────────────────────────────────
# 6) AUDIO PROCESSING CONSTANTS
# ──────────────────────────────────────────────────────────────────────────
TARGET_SAMPLE_RATE: int = 16000  # Hz — required by Whisper


def validate_api_keys() -> None:
    """Print a warning for any missing API key.

    Called at pipeline start-up so the user finds out immediately instead
    of after waiting several minutes for transcription to finish.
    """
    if not ARABIC_MODEL_API_KEY:
        print("WARNING: MISTRAL_API_KEY is not set. The summarization step will fail.")
    if not GEMINI_API_KEY:
        print("WARNING: GEMINI_API_KEY is not set. The summarization step will fail.")
