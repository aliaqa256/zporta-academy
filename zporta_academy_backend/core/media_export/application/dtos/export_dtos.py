"""
Media & Document Export Application DTOs.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ExportLessonCommand:
    """Command requesting a lesson export."""
    lesson_id: int
    format: str = "pdf"
    user_id: int = 0
    is_staff: bool = False


@dataclass(frozen=True)
class ExportResultDTO:
    """Result containing rendered binary bytes, content-type and filename."""
    file_bytes: bytes
    mime_type: str
    filename: str
    size_bytes: int
