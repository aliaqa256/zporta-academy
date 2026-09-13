"""
Media Storage Outbound Port Interface.
"""
from abc import ABC, abstractmethod
from typing import Optional


class MediaStoragePort(ABC):
    """Outbound port for persisting and retrieving exported media files."""

    @abstractmethod
    def save_file(self, relative_path: str, file_bytes: bytes) -> str:
        """Save bytes to storage and return accessible URI or file path."""
        pass

    @abstractmethod
    def read_file(self, relative_path: str) -> Optional[bytes]:
        """Read file bytes from storage."""
        pass

    @abstractmethod
    def file_exists(self, relative_path: str) -> bool:
        """Check if file exists in storage."""
        pass
