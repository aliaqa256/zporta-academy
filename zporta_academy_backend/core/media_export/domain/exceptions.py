"""
Media & Document Export Domain Exceptions.
"""
from core.shared_kernel.domain.exceptions import DomainException


class ExportError(DomainException):
    """Base domain exception for media and document export errors."""
    pass


class UnsupportedExportFormatError(ExportError):
    """Raised when an unsupported export format is requested."""
    def __init__(self, format_name: str):
        super().__init__(f"Unsupported export format: '{format_name}'.")
        self.format_name = format_name


class RenderingError(ExportError):
    """Raised when document rendering (PDF or Word) fails."""
    pass


class MediaStorageError(ExportError):
    """Raised when file storage operations fail."""
    pass
