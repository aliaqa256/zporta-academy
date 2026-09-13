from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from bulk_import.domain.entities import BulkImportJobEntity


class BulkImportRepositoryPort(ABC):
    """Abstract port for persisting bulk import jobs and ingested entities."""

    @abstractmethod
    def create_import_job(
        self,
        user_id: int,
        total_courses: int,
        total_lessons: int,
        total_quizzes: int,
        total_questions: int
    ) -> BulkImportJobEntity:
        pass

    @abstractmethod
    def execute_curriculum_ingestion(
        self,
        job_id: str,
        user_id: int,
        payload: Dict[str, Any]
    ) -> BulkImportJobEntity:
        pass
