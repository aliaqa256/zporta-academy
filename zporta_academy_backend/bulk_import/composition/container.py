from bulk_import.application.ports.outbound.bulk_import_repository_port import BulkImportRepositoryPort
from bulk_import.application.use_cases.validate_and_import_curriculum import ValidateAndImportCurriculumUseCase
from bulk_import.adapters.outbound.persistence.django_bulk_import_repository import DjangoBulkImportRepository


def build_bulk_import_repository() -> BulkImportRepositoryPort:
    return DjangoBulkImportRepository()


def build_validate_and_import_curriculum_use_case(
    repository: BulkImportRepositoryPort = None
) -> ValidateAndImportCurriculumUseCase:
    return ValidateAndImportCurriculumUseCase(
        repository=repository or build_bulk_import_repository()
    )
