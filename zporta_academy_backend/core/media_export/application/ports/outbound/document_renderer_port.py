"""
Document Renderer Outbound Port Interface.
"""
from abc import ABC, abstractmethod
from core.media_export.domain.entities import DocumentExportEntity


class DocumentRendererPort(ABC):
    """Outbound port for rendering lesson documents into PDF or Word format."""

    @abstractmethod
    def render_pdf(self, document: DocumentExportEntity) -> bytes:
        """Render document entity into PDF binary bytes."""
        pass

    @abstractmethod
    def render_docx(self, document: DocumentExportEntity) -> bytes:
        """Render document entity into DOCX binary bytes."""
        pass
