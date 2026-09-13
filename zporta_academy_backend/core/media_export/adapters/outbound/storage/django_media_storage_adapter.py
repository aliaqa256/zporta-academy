"""
Django Media Storage Adapter.
"""
import os
from typing import Optional
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from core.media_export.application.ports.outbound.media_storage_port import MediaStoragePort


class DjangoMediaStorageAdapter(MediaStoragePort):
    """Local filesystem or S3 storage adapter for exported documents and media."""

    def save_file(self, relative_path: str, file_bytes: bytes) -> str:
        saved_path = default_storage.save(relative_path, ContentFile(file_bytes))
        return default_storage.url(saved_path)

    def read_file(self, relative_path: str) -> Optional[bytes]:
        if not default_storage.exists(relative_path):
            return None
        with default_storage.open(relative_path, "rb") as f:
            return f.read()

    def file_exists(self, relative_path: str) -> bool:
        return default_storage.exists(relative_path)
