"""
Media & Document Export Composition Container.
"""
from core.media_export.adapters.outbound.renderers.weasyprint_renderer_adapter import WeasyPrintRendererAdapter
from core.media_export.adapters.outbound.storage.django_media_storage_adapter import DjangoMediaStorageAdapter
from core.media_export.application.ports.outbound.document_renderer_port import DocumentRendererPort
from core.media_export.application.ports.outbound.media_storage_port import MediaStoragePort
from core.media_export.application.use_cases.export_lesson_document import ExportLessonDocumentUseCase


def build_document_renderer_adapter() -> DocumentRendererPort:
    return WeasyPrintRendererAdapter()


def build_media_storage_adapter() -> MediaStoragePort:
    return DjangoMediaStorageAdapter()


def build_export_lesson_document_use_case(
    renderer: DocumentRendererPort = None,
) -> ExportLessonDocumentUseCase:
    return ExportLessonDocumentUseCase(
        renderer=renderer or build_document_renderer_adapter()
    )
