"""
Media & Document Export Domain Entities.
"""
from dataclasses import dataclass, field
from typing import Optional
from core.shared_kernel.domain.base_entity import BaseEntity
from core.media_export.domain.value_objects import ExportFormat, MediaType


@dataclass(eq=False)
class DocumentExportEntity(BaseEntity[Optional[int]]):
    """Represents a lesson or content entity ready for document export."""
    id: Optional[int] = None
    title: str = ""
    content_html: str = ""
    author_name: str = ""
    created_at_str: str = ""
    subject_name: Optional[str] = None
    course_title: Optional[str] = None
    accent_color: str = "#222E3B"
    custom_css: str = ""
    video_url: Optional[str] = None


@dataclass(frozen=True)
class ExportResultEntity:
    """Represents the rendered export artifact."""
    file_bytes: bytes
    mime_type: str
    filename: str
    size_bytes: int


@dataclass(eq=False)
class MediaAssetEntity(BaseEntity[Optional[int]]):
    """Represents a stored media file or asset."""
    id: Optional[int] = None
    title: str = ""
    file_url: str = ""
    media_type: MediaType = MediaType.DOCUMENT
    file_size_bytes: int = 0
    created_by_id: Optional[int] = None
