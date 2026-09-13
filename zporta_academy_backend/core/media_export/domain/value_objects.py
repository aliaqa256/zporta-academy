"""
Media & Document Export Domain Value Objects.
"""
from enum import Enum


class ExportFormat(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    AUDIO_ZIP = "audio_zip"


class MediaType(str, Enum):
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    DOCUMENT = "document"
