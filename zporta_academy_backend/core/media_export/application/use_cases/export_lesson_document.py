"""
Export Lesson Document Use Case.
"""
from core.media_export.application.dtos.export_dtos import ExportLessonCommand, ExportResultDTO
from core.media_export.application.ports.outbound.document_renderer_port import DocumentRendererPort
from core.media_export.domain.entities import DocumentExportEntity
from core.media_export.domain.exceptions import UnsupportedExportFormatError
from core.media_export.domain.policies import ExportFilenamePolicy
from core.media_export.domain.value_objects import ExportFormat


class ExportLessonDocumentUseCase:
    """Use case to orchestrate rendering a lesson entity into requested export format."""

    def __init__(self, renderer: DocumentRendererPort):
        self._renderer = renderer

    def execute(self, doc_entity: DocumentExportEntity, format_type: str = "pdf") -> ExportResultDTO:
        fmt = (format_type or "pdf").lower()

        if fmt == ExportFormat.PDF.value:
            file_bytes = self._renderer.render_pdf(doc_entity)
            mime_type = "application/pdf"
            filename = ExportFilenamePolicy.generate_filename(doc_entity.id or 0, "pdf", doc_entity.title)
        elif fmt == ExportFormat.DOCX.value:
            file_bytes = self._renderer.render_docx(doc_entity)
            mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            filename = ExportFilenamePolicy.generate_filename(doc_entity.id or 0, "docx", doc_entity.title)
        else:
            raise UnsupportedExportFormatError(fmt)

        return ExportResultDTO(
            file_bytes=file_bytes,
            mime_type=mime_type,
            filename=filename,
            size_bytes=len(file_bytes),
        )
