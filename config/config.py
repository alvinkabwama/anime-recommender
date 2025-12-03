from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# --- Project Root ---
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# --- Groq API ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "llama-3.1-8B-instant")

# --- HuggingFace Model Config ---
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

HUGGINGFACE_MODEL_NAME = os.getenv("HUGGINGFACE_MODEL_NAME", "intfloat/e5-large-v2")

# This ensures the models folder is ALWAYS at repo root
HUGGINGFACE_MODEL_CACHE_DIR = PROJECT_ROOT / "models" / "e5-large-v2"
