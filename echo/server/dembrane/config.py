# This configuration file implements a robust environment-based configuration
# system with built-in logging. It follows a "fail-fast" pattern by asserting
# required environment variables and provides sensible defaults for optional ones.

# 2025-06-05 FIXME: file's messy / needs a refactor. potential config management via yaml config?
# patterns are inconsistent - ENABLE_LITELLM_WHISPER_TRANSCRIPTION needs to be set
# better yet modularize it and have modules manage their own config?

## ENABLE_ASSEMBLYAI_TRANSCRIPTION = os.environ.get(
# "ENABLE_ASSEMBLYAI_TRANSCRIPTION", "false"
# ).lower() in ["true", "1"]
# This is a bad pattern for hygiene because it allows for multiple values to be set if you want it to be true/false

# This file inits twice for some reason...

import os
import sys
import logging
from typing import Literal, cast

try:
    import colorlog

    has_colorlog = True
except ImportError:
    has_colorlog = False

import dotenv

if has_colorlog:
    handler = colorlog.StreamHandler(sys.stdout)
    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)s:%(name)s:%(message)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )
    )
    logger = colorlog.getLogger("config")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # Set up the root logger too
    root_logger = colorlog.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)
else:
    # Fall back to basic configuration if colorlog is not available
    logging.basicConfig(level=logging.INFO, force=True)
    logger = logging.getLogger("config")

BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
dotenv_path = os.path.join(BASE_DIR, ".env")

if os.path.exists(dotenv_path):
    logger.info(f"loading environment variables from {dotenv_path}")
    dotenv.load_dotenv(dotenv_path, verbose=True, override=True)

DEBUG_MODE = os.environ.get("DEBUG_MODE", "false").lower() in ["true", "1"]
logger.info(f"DEBUG_MODE: {DEBUG_MODE}")
if DEBUG_MODE:
    # everything is debug if debug mode is enabled
    logging.getLogger().setLevel(logging.DEBUG)
    # set the current logger to debug
    logger.setLevel(logging.DEBUG)

API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")
logger.debug(f"API_BASE_URL: {API_BASE_URL}")

ADMIN_BASE_URL = os.environ.get("ADMIN_BASE_URL", "http://localhost:3000")
logger.debug(f"ADMIN_BASE_URL: {ADMIN_BASE_URL}")

PARTICIPANT_BASE_URL = os.environ.get("PARTICIPANT_BASE_URL", "http://localhost:3001")
logger.debug(f"PARTICIPANT_BASE_URL: {PARTICIPANT_BASE_URL}")

DIRECTUS_BASE_URL = os.environ.get("DIRECTUS_BASE_URL", "http://directus:8055")
logger.debug(f"DIRECTUS_BASE_URL: {DIRECTUS_BASE_URL}")

DISABLE_REDACTION = os.environ.get("DISABLE_REDACTION", "false").lower() in ["true", "1"]
logger.debug(f"DISABLE_REDACTION: {DISABLE_REDACTION}")

DISABLE_CHAT_TITLE_GENERATION = os.environ.get(
    "DISABLE_CHAT_TITLE_GENERATION", "false"
).lower() in [
    "true",
    "1",
]
logger.debug(f"DISABLE_CHAT_TITLE_GENERATION: {DISABLE_CHAT_TITLE_GENERATION}")

PROMPT_TEMPLATES_DIR = os.path.join(BASE_DIR, "prompt_templates")
logger.debug(f"PROMPT_TEMPLATES_DIR: {PROMPT_TEMPLATES_DIR}")

JSON_TEMPLATES_DIR = os.path.join(BASE_DIR, "json_templates")
logger.debug(f"JSON_TEMPLATES_DIR: {JSON_TEMPLATES_DIR}")

DIRECTUS_SECRET = os.environ.get("DIRECTUS_SECRET")
assert DIRECTUS_SECRET, "DIRECTUS_SECRET environment variable is not set"
logger.debug("DIRECTUS_SECRET: set")

DIRECTUS_TOKEN = os.environ.get("DIRECTUS_TOKEN")
assert DIRECTUS_TOKEN, "DIRECTUS_TOKEN environment variable is not set"
logger.debug("DIRECTUS_TOKEN: set")

DIRECTUS_SESSION_COOKIE_NAME = os.environ.get(
    "DIRECTUS_SESSION_COOKIE_NAME", "directus_session_token"
)
logger.debug(f"DIRECTUS_SESSION_COOKIE_NAME: {DIRECTUS_SESSION_COOKIE_NAME}")

DATABASE_URL = os.environ.get("DATABASE_URL")
assert DATABASE_URL, "DATABASE_URL environment variable is not set"
logger.debug("DATABASE_URL: set")

if not DATABASE_URL.startswith("postgresql+psycopg://"):
    logger.warning("DATABASE_URL is not a postgresql+psycopg:// URL, attempting to fix it...")
    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://")
    else:
        raise ValueError("DATABASE_URL is not valid (we need a postgresql+psycopg URL)")

REDIS_URL = os.environ.get("REDIS_URL")
assert REDIS_URL, "REDIS_URL environment variable is not set"
logger.debug("REDIS_URL: set")

OPENAI_API_BASE_URL = os.environ.get("OPENAI_API_BASE_URL", "https://api.openai.com/v1")
logger.debug(f"OPENAI_API_BASE_URL: {OPENAI_API_BASE_URL}")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
assert OPENAI_API_KEY, "OPENAI_API_KEY environment variable is not set"
logger.debug("OPENAI_API_KEY: set")

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
assert ANTHROPIC_API_KEY, "ANTHROPIC_API_KEY environment variable is not set"
logger.debug("ANTHROPIC_API_KEY: set")

ANTHROPIC_CHAT_MODEL = os.environ.get("ANTHROPIC_CHAT_MODEL")
assert ANTHROPIC_CHAT_MODEL, "ANTHROPIC_CHAT_MODEL environment variable is not set"
logger.debug(f"ANTHROPIC_CHAT_MODEL: {ANTHROPIC_CHAT_MODEL}")

SERVE_API_DOCS = os.environ.get("SERVE_API_DOCS", "false").lower() in ["true", "1"]
logger.debug(f"SERVE_API_DOCS: {SERVE_API_DOCS}")

DISABLE_SENTRY = os.environ.get("DISABLE_SENTRY", "false").lower() in ["true", "1"]
logger.debug(f"DISABLE_SENTRY: {DISABLE_SENTRY}")

BUILD_VERSION = os.environ.get("BUILD_VERSION", "dev")
logger.debug(f"BUILD_VERSION: {BUILD_VERSION}")

ENVIRONMENT = "development"
if BUILD_VERSION != "dev":
    ENVIRONMENT = "production"
logger.debug(f"ENVIRONMENT: {ENVIRONMENT}")

# Neo4j configuration
NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
logger.debug(f"NEO4J_URI: {NEO4J_URI}")

NEO4J_USERNAME = os.environ.get("NEO4J_USERNAME", "neo4j")
logger.debug(f"NEO4J_USERNAME: {NEO4J_USERNAME}")

NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "admin@dembrane")
logger.debug("NEO4J_PASSWORD: set")

STORAGE_S3_BUCKET = os.environ.get("STORAGE_S3_BUCKET")
assert STORAGE_S3_BUCKET, "STORAGE_S3_BUCKET environment variable is not set"
logger.debug("STORAGE_S3_BUCKET: set")

STORAGE_S3_REGION = os.environ.get("STORAGE_S3_REGION", None)
logger.debug(f"STORAGE_S3_REGION: {STORAGE_S3_REGION}")
if STORAGE_S3_REGION is None:
    logger.warning("STORAGE_S3_REGION is not set, using 'None'")

STORAGE_S3_ENDPOINT = os.environ.get("STORAGE_S3_ENDPOINT")
assert STORAGE_S3_ENDPOINT, "STORAGE_S3_ENDPOINT environment variable is not set"
logger.debug("STORAGE_S3_ENDPOINT: set")

STORAGE_S3_KEY = os.environ.get("STORAGE_S3_KEY")
assert STORAGE_S3_KEY, "STORAGE_S3_KEY environment variable is not set"
logger.debug("STORAGE_S3_KEY: set")

STORAGE_S3_SECRET = os.environ.get("STORAGE_S3_SECRET")
assert STORAGE_S3_SECRET, "STORAGE_S3_SECRET environment variable is not set"
logger.debug("STORAGE_S3_SECRET: set")

DISABLE_CORS = os.environ.get("DISABLE_CORS", "false").lower() in ["true", "1"]
logger.debug(f"DISABLE_CORS: {DISABLE_CORS}")

### Transcription

TranscriptionProvider = Literal["Runpod", "LiteLLM", "AssemblyAI", "Dembrane-25-09"]
_ALLOWED_TRANSCRIPTION_PROVIDERS: set[str] = {
    "Runpod",
    "LiteLLM",
    "AssemblyAI",
    "Dembrane-25-09",
}

TRANSCRIPTION_PROVIDER_RAW: str | None = os.environ.get("TRANSCRIPTION_PROVIDER")
if not TRANSCRIPTION_PROVIDER_RAW:
    TRANSCRIPTION_PROVIDER: TranscriptionProvider | None = None
    logger.debug("TRANSCRIPTION_PROVIDER: not set")
else:
    if TRANSCRIPTION_PROVIDER_RAW not in _ALLOWED_TRANSCRIPTION_PROVIDERS:
        raise ValueError(
            f"TRANSCRIPTION_PROVIDER is not valid: {TRANSCRIPTION_PROVIDER_RAW}. "
            f"Allowed: {', '.join(sorted(_ALLOWED_TRANSCRIPTION_PROVIDERS))}"
        )
    TRANSCRIPTION_PROVIDER = cast(TranscriptionProvider, TRANSCRIPTION_PROVIDER_RAW)
    logger.debug(f"TRANSCRIPTION_PROVIDER: {TRANSCRIPTION_PROVIDER}")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    logger.debug("GEMINI_API_KEY: set")
else:
    logger.debug("GEMINI_API_KEY: not set")

ENABLE_ASSEMBLYAI_TRANSCRIPTION = os.environ.get(
    "ENABLE_ASSEMBLYAI_TRANSCRIPTION", "false"
).lower() in ["true", "1"]
logger.debug(f"ENABLE_ASSEMBLYAI_TRANSCRIPTION: {ENABLE_ASSEMBLYAI_TRANSCRIPTION}")

ASSEMBLYAI_API_KEY = os.environ.get("ASSEMBLYAI_API_KEY")
if ENABLE_ASSEMBLYAI_TRANSCRIPTION:
    assert ASSEMBLYAI_API_KEY, "ASSEMBLYAI_API_KEY environment variable is not set"
    logger.debug("ASSEMBLYAI_API_KEY: set")

ASSEMBLYAI_BASE_URL = os.environ.get("ASSEMBLYAI_BASE_URL", "https://api.eu.assemblyai.com")
logger.debug(f"ASSEMBLYAI_BASE_URL: {ASSEMBLYAI_BASE_URL}")

ENABLE_RUNPOD_WHISPER_TRANSCRIPTION = os.environ.get(
    "ENABLE_RUNPOD_WHISPER_TRANSCRIPTION", "false"
).lower() in ["true", "1"]
logger.debug(f"ENABLE_RUNPOD_WHISPER_TRANSCRIPTION: {ENABLE_RUNPOD_WHISPER_TRANSCRIPTION}")

RUNPOD_WHISPER_API_KEY = os.environ.get("RUNPOD_WHISPER_API_KEY")
if ENABLE_RUNPOD_WHISPER_TRANSCRIPTION:
    assert RUNPOD_WHISPER_API_KEY, "RUNPOD_WHISPER_API_KEY environment variable is not set"
    logger.debug("RUNPOD_WHISPER_API_KEY: set")

RUNPOD_WHISPER_BASE_URL = os.environ.get("RUNPOD_WHISPER_BASE_URL")
if ENABLE_RUNPOD_WHISPER_TRANSCRIPTION:
    assert RUNPOD_WHISPER_BASE_URL, "RUNPOD_WHISPER_BASE_URL environment variable is not set"
    logger.debug(f"RUNPOD_WHISPER_BASE_URL: {RUNPOD_WHISPER_BASE_URL}")

RUNPOD_WHISPER_PRIORITY_BASE_URL = os.environ.get("RUNPOD_WHISPER_PRIORITY_BASE_URL")
if ENABLE_RUNPOD_WHISPER_TRANSCRIPTION:
    assert RUNPOD_WHISPER_PRIORITY_BASE_URL, (
        "RUNPOD_WHISPER_PRIORITY_BASE_URL environment variable is not set"
    )
    logger.debug(f"RUNPOD_WHISPER_PRIORITY_BASE_URL: {RUNPOD_WHISPER_PRIORITY_BASE_URL}")

RUNPOD_WHISPER_MAX_REQUEST_THRESHOLD = int(
    str(os.environ.get("RUNPOD_WHISPER_MAX_REQUEST_THRESHOLD"))
)

ENABLE_LITELLM_WHISPER_TRANSCRIPTION = os.environ.get(
    "ENABLE_LITELLM_WHISPER_TRANSCRIPTION", "false"
).lower() in ["true", "1"]
logger.debug(f"ENABLE_LITELLM_WHISPER_TRANSCRIPTION: {ENABLE_LITELLM_WHISPER_TRANSCRIPTION}")

LITELLM_WHISPER_API_KEY = os.environ.get("LITELLM_WHISPER_API_KEY")
if ENABLE_LITELLM_WHISPER_TRANSCRIPTION:
    assert LITELLM_WHISPER_API_KEY, "LITELLM_WHISPER_API_KEY environment variable is not set"
    logger.debug("LITELLM_WHISPER_API_KEY: set")

LITELLM_WHISPER_API_VERSION = os.environ.get("LITELLM_WHISPER_API_VERSION", "2024-06-01")
if ENABLE_LITELLM_WHISPER_TRANSCRIPTION:
    assert LITELLM_WHISPER_API_VERSION, (
        "LITELLM_WHISPER_API_VERSION environment variable is not set"
    )
    logger.debug(f"LITELLM_WHISPER_API_VERSION: {LITELLM_WHISPER_API_VERSION}")

LITELLM_WHISPER_MODEL = os.environ.get("LITELLM_WHISPER_MODEL")
if ENABLE_LITELLM_WHISPER_TRANSCRIPTION:
    assert LITELLM_WHISPER_MODEL, "LITELLM_WHISPER_MODEL environment variable is not set"
    logger.debug(f"LITELLM_WHISPER_MODEL: {LITELLM_WHISPER_MODEL}")

LITELLM_WHISPER_URL = os.environ.get("LITELLM_WHISPER_URL")
if ENABLE_LITELLM_WHISPER_TRANSCRIPTION:
    assert LITELLM_WHISPER_URL, "LITELLM_WHISPER_URL environment variable is not set"
    logger.debug(f"LITELLM_WHISPER_URL: {LITELLM_WHISPER_URL}")

### END Transcription

RUNPOD_TOPIC_MODELER_URL = os.environ.get("RUNPOD_TOPIC_MODELER_URL")
logger.debug(f"RUNPOD_TOPIC_MODELER_URL: {RUNPOD_TOPIC_MODELER_URL}")

RUNPOD_TOPIC_MODELER_API_KEY = os.environ.get("RUNPOD_TOPIC_MODELER_API_KEY")
if RUNPOD_TOPIC_MODELER_URL:
    assert RUNPOD_TOPIC_MODELER_API_KEY, (
        "RUNPOD_TOPIC_MODELER_API_KEY environment variable is not set"
    )
    logger.debug("RUNPOD_TOPIC_MODELER_API_KEY: set")

if ENABLE_RUNPOD_WHISPER_TRANSCRIPTION:
    assert RUNPOD_WHISPER_MAX_REQUEST_THRESHOLD, (
        "RUNPOD_WHISPER_MAX_REQUEST_THRESHOLD environment variable is not set"
    )
    logger.debug(f"RUNPOD_WHISPER_MAX_REQUEST_THRESHOLD: {RUNPOD_WHISPER_MAX_REQUEST_THRESHOLD}")

SMALL_LITELLM_MODEL = os.environ.get("SMALL_LITELLM_MODEL")  # 4o-mini
assert SMALL_LITELLM_MODEL, "SMALL_LITELLM_MODEL environment variable is not set"
logger.debug(f"SMALL_LITELLM_MODEL: {SMALL_LITELLM_MODEL}")

SMALL_LITELLM_API_KEY = os.environ.get("SMALL_LITELLM_API_KEY")
assert SMALL_LITELLM_API_KEY, "SMALL_LITELLM_API_KEY environment variable is not set"
logger.debug("SMALL_LITELLM_API_KEY: set")

SMALL_LITELLM_API_VERSION = os.environ.get("SMALL_LITELLM_API_VERSION")
assert SMALL_LITELLM_API_VERSION, "SMALL_LITELLM_API_VERSION environment variable is not set"
logger.debug(f"SMALL_LITELLM_API_VERSION: {SMALL_LITELLM_API_VERSION}")

SMALL_LITELLM_API_BASE = os.environ.get("SMALL_LITELLM_API_BASE")
assert SMALL_LITELLM_API_BASE, "SMALL_LITELLM_API_BASE environment variable is not set"
logger.debug(f"SMALL_LITELLM_API_BASE: {SMALL_LITELLM_API_BASE}")

MEDIUM_LITELLM_MODEL = os.environ.get("MEDIUM_LITELLM_MODEL")  # 4.1
assert MEDIUM_LITELLM_MODEL, "MEDIUM_LITELLM_MODEL environment variable is not set"
logger.debug(f"MEDIUM_LITELLM_MODEL: {MEDIUM_LITELLM_MODEL}")

MEDIUM_LITELLM_API_KEY = os.environ.get("MEDIUM_LITELLM_API_KEY")
assert MEDIUM_LITELLM_API_KEY, "MEDIUM_LITELLM_API_KEY environment variable is not set"
logger.debug("MEDIUM_LITELLM_API_KEY: set")

MEDIUM_LITELLM_API_VERSION = os.environ.get("MEDIUM_LITELLM_API_VERSION")
assert MEDIUM_LITELLM_API_VERSION, "MEDIUM_LITELLM_API_VERSION environment variable is not set"
logger.debug(f"MEDIUM_LITELLM_API_VERSION: {MEDIUM_LITELLM_API_VERSION}")

MEDIUM_LITELLM_API_BASE = os.environ.get("MEDIUM_LITELLM_API_BASE")
assert MEDIUM_LITELLM_API_BASE, "MEDIUM_LITELLM_API_BASE environment variable is not set"
logger.debug(f"MEDIUM_LITELLM_API_BASE: {MEDIUM_LITELLM_API_BASE}")

LARGE_LITELLM_MODEL = os.environ.get("LARGE_LITELLM_MODEL")  # o4-mini
assert LARGE_LITELLM_MODEL, "LARGE_LITELLM_MODEL environment variable is not set"
logger.debug(f"LARGE_LITELLM_MODEL: {LARGE_LITELLM_MODEL}")

LARGE_LITELLM_API_KEY = os.environ.get("LARGE_LITELLM_API_KEY")
assert LARGE_LITELLM_API_KEY, "LARGE_LITELLM_API_KEY environment variable is not set"
logger.debug("LARGE_LITELLM_API_KEY: set")

LARGE_LITELLM_API_VERSION = os.environ.get("LARGE_LITELLM_API_VERSION")
assert LARGE_LITELLM_API_VERSION, "LARGE_LITELLM_API_VERSION environment variable is not set"
logger.debug(f"LARGE_LITELLM_API_VERSION: {LARGE_LITELLM_API_VERSION}")

LARGE_LITELLM_API_BASE = os.environ.get("LARGE_LITELLM_API_BASE")
assert LARGE_LITELLM_API_BASE, "LARGE_LITELLM_API_BASE environment variable is not set"
logger.debug(f"LARGE_LITELLM_API_BASE: {LARGE_LITELLM_API_BASE}")

# *****************LIGHTRAG CONFIGURATIONS*****************

# Lightrag LLM model: Makes nodes and answers queries
LIGHTRAG_LITELLM_MODEL = os.environ.get("LIGHTRAG_LITELLM_MODEL")  # azure/gpt-4o-mini
assert LIGHTRAG_LITELLM_MODEL, "LIGHTRAG_LITELLM_MODEL environment variable is not set"
logger.debug(f"LIGHTRAG_LITELLM_MODEL: {LIGHTRAG_LITELLM_MODEL}")

LIGHTRAG_LITELLM_API_KEY = os.environ.get("LIGHTRAG_LITELLM_API_KEY")
assert LIGHTRAG_LITELLM_API_KEY, "LIGHTRAG_LITELLM_API_KEY environment variable is not set"
logger.debug("LIGHTRAG_LITELLM_API_KEY: set")

LIGHTRAG_LITELLM_API_VERSION = os.environ.get("LIGHTRAG_LITELLM_API_VERSION")
assert LIGHTRAG_LITELLM_API_VERSION, "LIGHTRAG_LITELLM_API_VERSION environment variable is not set"
logger.debug(f"LIGHTRAG_LITELLM_API_VERSION: {LIGHTRAG_LITELLM_API_VERSION}")

LIGHTRAG_LITELLM_API_BASE = os.environ.get("LIGHTRAG_LITELLM_API_BASE")
assert LIGHTRAG_LITELLM_API_BASE, "LIGHTRAG_LITELLM_API_BASE environment variable is not set"
logger.debug(f"LIGHTRAG_LITELLM_API_BASE: {LIGHTRAG_LITELLM_API_BASE}")

# Lightrag Audio model: Transcribes audio and gets contextual transcript
LIGHTRAG_LITELLM_AUDIOMODEL_MODEL = os.environ.get("LIGHTRAG_LITELLM_AUDIOMODEL_MODEL")
assert LIGHTRAG_LITELLM_AUDIOMODEL_MODEL, (
    "LIGHTRAG_LITELLM_AUDIOMODEL_MODEL environment variable is not set"
)
logger.debug(f"LIGHTRAG_LITELLM_AUDIOMODEL_MODEL: {LIGHTRAG_LITELLM_AUDIOMODEL_MODEL}")

LIGHTRAG_LITELLM_AUDIOMODEL_API_BASE = os.environ.get("LIGHTRAG_LITELLM_AUDIOMODEL_API_BASE")
assert LIGHTRAG_LITELLM_AUDIOMODEL_API_BASE, (
    "LIGHTRAG_LITELLM_AUDIOMODEL_API_BASE environment variable is not set"
)
logger.debug(f"LIGHTRAG_LITELLM_AUDIOMODEL_API_BASE: {LIGHTRAG_LITELLM_AUDIOMODEL_API_BASE}")

LIGHTRAG_LITELLM_AUDIOMODEL_API_KEY = os.environ.get("LIGHTRAG_LITELLM_AUDIOMODEL_API_KEY")
assert LIGHTRAG_LITELLM_AUDIOMODEL_API_KEY, (
    "LIGHTRAG_LITELLM_AUDIOMODEL_API_KEY environment variable is not set"
)
logger.debug("LIGHTRAG_LITELLM_AUDIOMODEL_API_KEY: set")

LIGHTRAG_LITELLM_AUDIOMODEL_API_VERSION = os.environ.get("LIGHTRAG_LITELLM_AUDIOMODEL_API_VERSION")
assert LIGHTRAG_LITELLM_AUDIOMODEL_API_VERSION, (
    "LIGHTRAG_LITELLM_AUDIOMODEL_API_VERSION environment variable is not set"
)
logger.debug(f"LIGHTRAG_LITELLM_AUDIOMODEL_API_VERSION: {LIGHTRAG_LITELLM_AUDIOMODEL_API_VERSION}")


# Lightrag Text Structure model: Structures output from audio model
LIGHTRAG_LITELLM_TEXTSTRUCTUREMODEL_MODEL = os.environ.get(
    "LIGHTRAG_LITELLM_TEXTSTRUCTUREMODEL_MODEL"
)  # azure/gpt-4o-mini
assert LIGHTRAG_LITELLM_TEXTSTRUCTUREMODEL_MODEL, (
    "LIGHTRAG_LITELLM_TEXTSTRUCTUREMODEL_MODEL environment variable is not set"
)
logger.debug(
    f"LIGHTRAG_LITELLM_TEXTSTRUCTUREMODEL_MODEL: {LIGHTRAG_LITELLM_TEXTSTRUCTUREMODEL_MODEL}"
)

LIGHTRAG_LITELLM_TEXTSTRUCTUREMODEL_API_BASE = os.environ.get(
    "LIGHTRAG_LITELLM_TEXTSTRUCTUREMODEL_API_BASE"
)
assert LIGHTRAG_LITELLM_TEXTSTRUCTUREMODEL_API_BASE, (
    "LIGHTRAG_LITELLM_TEXTSTRUCTUREMODEL_API_BASE environment variable is not set"
)
logger.debug(
    f"LIGHTRAG_LITELLM_TEXTSTRUCTUREMODEL_API_BASE: {LIGHTRAG_LITELLM_TEXTSTRUCTUREMODEL_API_BASE}"
)

LIGHTRAG_LITELLM_TEXTSTRUCTUREMODEL_API_KEY = os.environ.get(
    "LIGHTRAG_LITELLM_TEXTSTRUCTUREMODEL_API_KEY"
)
assert LIGHTRAG_LITELLM_TEXTSTRUCTUREMODEL_API_KEY, (
    "LIGHTRAG_LITELLM_TEXTSTRUCTUREMODEL_API_KEY environment variable is not set"
)
logger.debug("LIGHTRAG_LITELLM_TEXTSTRUCTUREMODEL_API_KEY: set")

LIGHTRAG_LITELLM_TEXTSTRUCTUREMODEL_API_VERSION = os.environ.get(
    "LIGHTRAG_LITELLM_TEXTSTRUCTUREMODEL_API_VERSION"
)
assert LIGHTRAG_LITELLM_TEXTSTRUCTUREMODEL_API_VERSION, (
    "LIGHTRAG_LITELLM_TEXTSTRUCTUREMODEL_API_VERSION environment variable is not set"
)
logger.debug(
    f"LIGHTRAG_LITELLM_TEXTSTRUCTUREMODEL_API_VERSION: {LIGHTRAG_LITELLM_TEXTSTRUCTUREMODEL_API_VERSION}"
)

# Lightrag Embedding model: Embeds text
LIGHTRAG_LITELLM_EMBEDDING_MODEL = os.environ.get(
    "LIGHTRAG_LITELLM_EMBEDDING_MODEL"
)  # azure/text-embedding-ada-002
assert LIGHTRAG_LITELLM_EMBEDDING_MODEL, (
    "LIGHTRAG_LITELLM_EMBEDDING_MODEL environment variable is not set"
)
logger.debug(f"LIGHTRAG_LITELLM_EMBEDDING_MODEL: {LIGHTRAG_LITELLM_EMBEDDING_MODEL}")

LIGHTRAG_LITELLM_EMBEDDING_API_BASE = os.environ.get("LIGHTRAG_LITELLM_EMBEDDING_API_BASE")
assert LIGHTRAG_LITELLM_EMBEDDING_API_BASE, (
    "LIGHTRAG_LITELLM_EMBEDDING_API_BASE environment variable is not set"
)
logger.debug(f"LIGHTRAG_LITELLM_EMBEDDING_API_BASE: {LIGHTRAG_LITELLM_EMBEDDING_API_BASE}")

LIGHTRAG_LITELLM_EMBEDDING_API_KEY = os.environ.get("LIGHTRAG_LITELLM_EMBEDDING_API_KEY")
assert LIGHTRAG_LITELLM_EMBEDDING_API_KEY, (
    "LIGHTRAG_LITELLM_EMBEDDING_API_KEY environment variable is not set"
)
logger.debug("LIGHTRAG_LITELLM_EMBEDDING_API_KEY: set")

LIGHTRAG_LITELLM_EMBEDDING_API_VERSION = os.environ.get("LIGHTRAG_LITELLM_EMBEDDING_API_VERSION")
assert LIGHTRAG_LITELLM_EMBEDDING_API_VERSION, (
    "LIGHTRAG_LITELLM_EMBEDDING_API_VERSION environment variable is not set"
)
logger.debug(f"LIGHTRAG_LITELLM_EMBEDDING_API_VERSION: {LIGHTRAG_LITELLM_EMBEDDING_API_VERSION}")

LIGHTRAG_LITELLM_INFERENCE_MODEL = os.environ.get(
    "LIGHTRAG_LITELLM_INFERENCE_MODEL", "anthropic/claude-3-5-sonnet-20240620"
)
assert LIGHTRAG_LITELLM_INFERENCE_MODEL, (
    "LIGHTRAG_LITELLM_INFERENCE_MODEL environment variable is not set"
)
logger.debug(f"LIGHTRAG_LITELLM_INFERENCE_MODEL: {LIGHTRAG_LITELLM_INFERENCE_MODEL}")

LIGHTRAG_LITELLM_INFERENCE_API_KEY = os.environ.get("LIGHTRAG_LITELLM_INFERENCE_API_KEY")
assert LIGHTRAG_LITELLM_INFERENCE_API_KEY, (
    "LIGHTRAG_LITELLM_INFERENCE_API_KEY environment variable is not set"
)
logger.debug("LIGHTRAG_LITELLM_INFERENCE_API_KEY: set")

LIGHTRAG_LITELLM_INFERENCE_API_VERSION = os.environ.get("LIGHTRAG_LITELLM_INFERENCE_API_VERSION")
if LIGHTRAG_LITELLM_INFERENCE_API_VERSION:
    logger.debug(
        f"LIGHTRAG_LITELLM_INFERENCE_API_VERSION: {LIGHTRAG_LITELLM_INFERENCE_API_VERSION}"
    )
else:
    logger.debug("LIGHTRAG_LITELLM_INFERENCE_API_VERSION: not set")

LIGHTRAG_LITELLM_INFERENCE_API_BASE = os.environ.get("LIGHTRAG_LITELLM_INFERENCE_API_BASE")
if LIGHTRAG_LITELLM_INFERENCE_API_BASE:
    logger.debug(f"LIGHTRAG_LITELLM_INFERENCE_API_BASE: {LIGHTRAG_LITELLM_INFERENCE_API_BASE}")
else:
    logger.debug("LIGHTRAG_LITELLM_INFERENCE_API_BASE: not set")

DISABLE_MULTILINGUAL_DIARIZATION = os.environ.get(
    "DISABLE_MULTILINGUAL_DIARIZATION", "false"
).lower() in [
    "true",
    "1",
]
logger.debug(f"DISABLE_MULTILINGUAL_DIARIZATION: {DISABLE_MULTILINGUAL_DIARIZATION}")

ENABLE_RUNPOD_DIARIZATION = os.environ.get("ENABLE_RUNPOD_DIARIZATION", "false").lower() in [
    "true",
    "1",
]
logger.debug(f"ENABLE_RUNPOD_DIARIZATION: {ENABLE_RUNPOD_DIARIZATION}")

RUNPOD_DIARIZATION_API_KEY = os.environ.get("RUNPOD_DIARIZATION_API_KEY")
if ENABLE_RUNPOD_DIARIZATION:
    assert RUNPOD_DIARIZATION_API_KEY, "RUNPOD_DIARIZATION_API_KEY environment variable is not set"
    logger.debug("RUNPOD_DIARIZATION_API_KEY: set")

RUNPOD_DIARIZATION_BASE_URL = os.environ.get("RUNPOD_DIARIZATION_BASE_URL")
if ENABLE_RUNPOD_DIARIZATION:
    assert RUNPOD_DIARIZATION_BASE_URL, (
        "RUNPOD_DIARIZATION_BASE_URL environment variable is not set"
    )
    logger.debug(f"RUNPOD_DIARIZATION_BASE_URL: {RUNPOD_DIARIZATION_BASE_URL}")

RUNPOD_DIARIZATION_TIMEOUT = int(os.environ.get("RUNPOD_DIARIZATION_TIMEOUT", 30))
if ENABLE_RUNPOD_DIARIZATION:
    logger.debug(f"RUNPOD_DIARIZATION_TIMEOUT: {RUNPOD_DIARIZATION_TIMEOUT}")
# ---------------/Secrets---------------


# ---------------Configurations---------------
AUDIO_LIGHTRAG_CONVERSATION_HISTORY_NUM = int(
    os.environ.get("AUDIO_LIGHTRAG_CONVERSATION_HISTORY_NUM", 10)
)
assert AUDIO_LIGHTRAG_CONVERSATION_HISTORY_NUM, (
    "AUDIO_LIGHTRAG_CONVERSATION_HISTORY_NUM environment variable is not set"
)
logger.debug(f"AUDIO_LIGHTRAG_CONVERSATION_HISTORY_NUM: {AUDIO_LIGHTRAG_CONVERSATION_HISTORY_NUM}")

AUDIO_LIGHTRAG_COOL_OFF_TIME_SECONDS = int(
    os.environ.get("AUDIO_LIGHTRAG_COOL_OFF_TIME_SECONDS", 60)
)
assert AUDIO_LIGHTRAG_COOL_OFF_TIME_SECONDS, (
    "AUDIO_LIGHTRAG_COOL_OFF_TIME_SECONDS environment variable is not set"
)
logger.debug(f"AUDIO_LIGHTRAG_COOL_OFF_TIME_SECONDS: {AUDIO_LIGHTRAG_COOL_OFF_TIME_SECONDS}")

ENABLE_AUDIO_LIGHTRAG_INPUT = os.environ.get("ENABLE_AUDIO_LIGHTRAG_INPUT", "false").lower() in [
    "true",
    "1",
]
assert ENABLE_AUDIO_LIGHTRAG_INPUT is not None, (
    "ENABLE_AUDIO_LIGHTRAG_INPUT environment variable is not set"
)
logger.debug(f"ENABLE_AUDIO_LIGHTRAG_INPUT: {ENABLE_AUDIO_LIGHTRAG_INPUT}")

AUDIO_LIGHTRAG_MAX_AUDIO_FILE_SIZE_MB = int(
    os.environ.get("AUDIO_LIGHTRAG_MAX_AUDIO_FILE_SIZE_MB", 15)
)
assert AUDIO_LIGHTRAG_MAX_AUDIO_FILE_SIZE_MB, (
    "AUDIO_LIGHTRAG_MAX_AUDIO_FILE_SIZE_MB environment variable is not set"
)
logger.debug(f"AUDIO_LIGHTRAG_MAX_AUDIO_FILE_SIZE_MB: {AUDIO_LIGHTRAG_MAX_AUDIO_FILE_SIZE_MB}")

AUDIO_LIGHTRAG_TOP_K_PROMPT = int(os.environ.get("AUDIO_LIGHTRAG_TOP_K_PROMPT", 100))
assert AUDIO_LIGHTRAG_TOP_K_PROMPT, "AUDIO_LIGHTRAG_TOP_K_PROMPT environment variable is not set"
logger.debug(f"AUDIO_LIGHTRAG_TOP_K_PROMPT: {AUDIO_LIGHTRAG_TOP_K_PROMPT}")

ENABLE_CHAT_AUTO_SELECT = os.environ.get("ENABLE_CHAT_AUTO_SELECT", "false").lower() in [
    "true",
    "1",
]
assert ENABLE_CHAT_AUTO_SELECT is not None, (
    "ENABLE_CHAT_AUTO_SELECT environment variable is not set"
)
logger.debug(f"ENABLE_CHAT_AUTO_SELECT: {ENABLE_CHAT_AUTO_SELECT}")

# Redis lock configuration
AUDIO_LIGHTRAG_REDIS_LOCK_PREFIX = os.environ.get(
    "AUDIO_LIGHTRAG_REDIS_LOCK_PREFIX", "etl_lock_conv_"
)
assert AUDIO_LIGHTRAG_REDIS_LOCK_PREFIX, (
    "AUDIO_LIGHTRAG_REDIS_LOCK_PREFIX environment variable is not set"
)
logger.debug(f"AUDIO_LIGHTRAG_REDIS_LOCK_PREFIX: {AUDIO_LIGHTRAG_REDIS_LOCK_PREFIX}")

AUDIO_LIGHTRAG_REDIS_LOCK_EXPIRY = int(os.environ.get("AUDIO_LIGHTRAG_REDIS_LOCK_EXPIRY", 3600))
assert AUDIO_LIGHTRAG_REDIS_LOCK_EXPIRY, (
    "AUDIO_LIGHTRAG_REDIS_LOCK_EXPIRY environment variable is not set"
)
logger.debug(f"AUDIO_LIGHTRAG_REDIS_LOCK_EXPIRY: {AUDIO_LIGHTRAG_REDIS_LOCK_EXPIRY}")

LIGHTRAG_CONFIG_ID = os.environ.get("LIGHTRAG_CONFIG_ID", "default_lightrag_config_id")
assert LIGHTRAG_CONFIG_ID, "LIGHTRAG_CONFIG_ID environment variable is not set"
logger.debug(f"LIGHTRAG_CONFIG_ID: {LIGHTRAG_CONFIG_ID}")
# ---------------/Configurations---------------

# *****************/LIGHTRAG CONFIGURATIONS*****************


# hide some noisy loggers
for hide_logger in [
    "boto3",
    "botocore",
    "httpx",
    "httpcore",
    "LiteLLM",
    "openai",
    "requests",
    "psycopg",
    "s3transfer",
    "urllib3",
    "multipart",
]:
    logging.getLogger(hide_logger).setLevel(logging.WARNING)
