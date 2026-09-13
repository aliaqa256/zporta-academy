"""
Value objects and enums for AI Core domain.
Pure Python.
"""
from enum import Enum


class ModelProvider(str, Enum):
    OPENAI = "openai"
    GEMINI = "gemini"
    CLAUDE = "claude"
    ELEVENLABS = "elevenlabs"
    GOOGLE_TTS = "google_tts"
    LOCAL_SMALL_MODEL = "local_small_model"


class ModelTier(str, Enum):
    CHEAP = "cheap"
    NORMAL = "normal"
    PREMIUM = "premium"


class RequestType(str, Enum):
    LESSON_SCRIPT = "lesson_script"
    QUIZ_GENERATION = "quiz_generation"
    PODCAST_SCRIPT = "podcast_script"
    EMAIL_CONTENT = "email_content"
    REPORT = "report"
    TRANSLATION = "translation"
    TTS_AUDIO = "tts_audio"
    OTHER = "other"


class SelectionMode(str, Enum):
    AUTO = "auto"
    MANUAL = "manual"
