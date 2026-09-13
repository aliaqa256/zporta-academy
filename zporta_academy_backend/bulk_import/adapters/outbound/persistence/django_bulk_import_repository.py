from typing import Dict, Any, Optional
from django.contrib.auth import get_user_model
from bulk_import.domain.entities import BulkImportJobEntity
from bulk_import.application.ports.outbound.bulk_import_repository_port import BulkImportRepositoryPort
from bulk_import.models import BulkImportJob
from bulk_import.import_handler import BulkImportHandler

User = get_user_model()


class DjangoBulkImportRepository(BulkImportRepositoryPort):
    """Django ORM adapter for persisting bulk import jobs and handling ingestion."""

    def create_import_job(
        self,
        user_id: int,
        total_courses: int,
        total_lessons: int,
        total_quizzes: int,
        total_questions: int
    ) -> BulkImportJobEntity:
        job = BulkImportJob.objects.create(
            created_by_id=user_id,
            status="processing",
            total_courses=total_courses,
            total_lessons=total_lessons,
            total_quizzes=total_quizzes,
            total_questions=total_questions
        )
        return self._to_entity(job)

    def execute_curriculum_ingestion(
        self,
        job_id: str,
        user_id: int,
        payload: Dict[str, Any]
    ) -> BulkImportJobEntity:
        user = User.objects.get(id=user_id)
        job = BulkImportJob.objects.get(id=job_id)

        handler = BulkImportHandler(user=user, job=job, dry_run=False)
        try:
            handler.process(payload)
        except Exception as e:
            job.status = "failed"
            job.errors.append(str(e))
            job.save(update_fields=["status", "errors"])

        job.refresh_from_db()
        return self._to_entity(job)

    def _to_entity(self, job: BulkImportJob) -> BulkImportJobEntity:
        return BulkImportJobEntity(
            id=str(job.id),
            created_by_id=job.created_by_id,
            status=job.status,
            total_courses=job.total_courses,
            total_lessons=job.total_lessons,
            total_quizzes=job.total_quizzes,
            total_questions=job.total_questions,
            processed_courses=job.processed_courses,
            processed_lessons=job.processed_lessons,
            processed_quizzes=job.processed_quizzes,
            processed_questions=job.processed_questions,
            errors=job.errors or [],
            warnings=job.warnings or [],
            summary=job.summary or ""
        )
