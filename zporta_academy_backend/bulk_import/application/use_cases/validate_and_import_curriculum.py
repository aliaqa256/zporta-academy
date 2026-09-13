from typing import Dict, Any
from bulk_import.domain.policies import BulkImportValidationPolicy
from bulk_import.domain.exceptions import InvalidImportPayloadError
from ..dtos import ImportValidationDTO, ImportResultDTO
from ..ports.outbound.bulk_import_repository_port import BulkImportRepositoryPort


class ValidateAndImportCurriculumUseCase:
    """Validates schema and coordinates transactional ingestion of bulk curriculum data."""

    def __init__(self, repository: BulkImportRepositoryPort):
        self.repository = repository

    def validate_payload(self, data: Any) -> ImportValidationDTO:
        report = BulkImportValidationPolicy.validate_curriculum_payload(data)
        return ImportValidationDTO(
            is_valid=report.is_valid,
            errors=[{"path": e.path, "message": e.message} for e in report.errors],
            warnings=[{"path": w.path, "message": w.message} for w in report.warnings],
            total_courses=report.total_courses,
            total_lessons=report.total_lessons,
            total_quizzes=report.total_quizzes,
            total_questions=report.total_questions
        )

    def execute_import(self, user_id: int, payload: Dict[str, Any]) -> ImportResultDTO:
        val = self.validate_payload(payload)
        if not val.is_valid:
            error_msgs = [f"{e['path']}: {e['message']}" for e in val.errors]
            raise InvalidImportPayloadError("; ".join(error_msgs[:5]))

        job = self.repository.create_import_job(
            user_id=user_id,
            total_courses=val.total_courses,
            total_lessons=val.total_lessons,
            total_quizzes=val.total_quizzes,
            total_questions=val.total_questions
        )

        completed_job = self.repository.execute_curriculum_ingestion(
            job_id=job.id,
            user_id=user_id,
            payload=payload
        )

        return ImportResultDTO(
            success=(completed_job.status == "completed"),
            message=f"Bulk import finished with status {completed_job.status}",
            job_id=completed_job.id,
            total_courses=completed_job.processed_courses,
            total_lessons=completed_job.processed_lessons,
            total_quizzes=completed_job.processed_quizzes,
            total_questions=completed_job.processed_questions,
            errors=completed_job.errors
        )
