class BulkImportDomainError(Exception):
    """Base domain exception for bulk import."""
    pass


class InvalidImportPayloadError(BulkImportDomainError):
    """Raised when an import JSON payload fails schema validation."""
    pass
