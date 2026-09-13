"""
WeasyPrint PDF Renderer Adapter.
"""
import logging
from io import BytesIO
from core.media_export.application.ports.outbound.document_renderer_port import DocumentRendererPort
from core.media_export.domain.entities import DocumentExportEntity
from core.media_export.domain.exceptions import RenderingError
from core.media_export.domain.policies import HtmlSanitizationPolicy

logger = logging.getLogger(__name__)


class WeasyPrintRendererAdapter(DocumentRendererPort):
    """Renders high-fidelity PDF documents using WeasyPrint with full CSS & CJK support."""

    def render_pdf(self, document: DocumentExportEntity) -> bytes:
        html_string = HtmlSanitizationPolicy.build_printable_html(document)

        try:
            from weasyprint import HTML
            pdf_buffer = BytesIO()
            HTML(string=html_string).write_pdf(pdf_buffer)
            return pdf_buffer.getvalue()
        except ImportError:
            logger.warning("WeasyPrint not installed. Falling back to basic PDF generator.")
            return self._fallback_render_pdf(document)
        except Exception as e:
            logger.error(f"WeasyPrint rendering failed: {e}")
            raise RenderingError(f"WeasyPrint PDF render failure: {e}") from e

    def render_docx(self, document: DocumentExportEntity) -> bytes:
        # Delegate to docx adapter if called on this instance
        from core.media_export.adapters.outbound.renderers.docx_renderer_adapter import DocxRendererAdapter
        return DocxRendererAdapter().render_docx(document)

    def _fallback_render_pdf(self, document: DocumentExportEntity) -> bytes:
        """Basic PDF fallback if WeasyPrint encounters environmental issues."""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
            from bs4 import BeautifulSoup

            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            elements = [
                Paragraph(document.title, styles["Heading1"]),
                Paragraph(f"Author: {document.author_name}", styles["Normal"]),
                Spacer(1, 12),
            ]

            soup = BeautifulSoup(HtmlSanitizationPolicy.clean_html_for_export(document.content_html), "html.parser")
            for p in soup.get_text().split("\n"):
                if p.strip():
                    elements.append(Paragraph(p.strip(), styles["Normal"]))
                    elements.append(Spacer(1, 6))

            doc.build(elements)
            return buffer.getvalue()
        except Exception as e:
            raise RenderingError(f"Fallback PDF renderer failed: {e}") from e
