"""
Get Study Dashboard Use Case.
"""
from typing import Any, Dict, Optional
from learning.application.dtos.study_dtos import StudyDashboardDTO
from learning.application.ports.outbound.learning_repository_port import LearningRepositoryPort


class GetStudyDashboardUseCase:
    """Use case to build personalized dashboard recommendations for a student."""

    def __init__(self, repository: LearningRepositoryPort):
        self._repository = repository

    def execute(self, user_id: int, limit: int = 5, request_context: Optional[Dict[str, Any]] = None) -> StudyDashboardDTO:
        entity = self._repository.get_dashboard_aggregates(user_id, limit=limit, request_context=request_context)
        return StudyDashboardDTO(
            enrolled=entity.enrolled,
            suggested_courses=entity.suggested_courses,
            suggested_quizzes=entity.suggested_quizzes,
            next_lessons=entity.next_lessons,
            suggested_lessons=entity.suggested_lessons,
        )
