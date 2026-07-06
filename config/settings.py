"""
Application settings.

Centralized configuration loaded from environment variables.
"""

from pathlib import Path

import os
from dotenv import load_dotenv

load_dotenv()

os.environ["HF_HUB_DISABLE_XET"] = os.getenv(
    "HF_HUB_DISABLE_XET",
    "1"
)

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

BASE_DIR = Path(__file__).resolve().parent.parent

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))

COLLECTION_NAME = os.getenv("COLLECTION_NAME", "documents")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "BAAI/bge-m3"
)

RERANKER_MODEL = os.getenv(
    "RERANKER_MODEL",
    "BAAI/bge-reranker-v2-m3"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "mistral"
)

VECTOR_SIZE = int(
    os.getenv("VECTOR_SIZE", 1024)
)

HISTORY_TURNS = int(
    os.getenv("HISTORY_TURNS", 2)
)