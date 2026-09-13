"""
Django ORM implementation of QuizRepositoryPort.
"""
from typing import Optional, List
from django.db.models import Q
from quizzes.models import Quiz
from quizzes.domain.entities import QuizEntity
from quizzes.domain.value_objects import QuizType, QuizStatus, DifficultyLevel
from quizzes.application.dtos import QuizSummaryDTO
from quizzes.application.ports.outbound.quiz_repository_port import QuizRepositoryPort


class DjangoQuizRepository(QuizRepositoryPort):
    def get_by_id(self, quiz_id: int) -> Optional[QuizEntity]:
        try:
            m = Quiz.objects.select_related('subject', 'course', 'created_by').get(id=quiz_id)
            return self._to_entity(m)
        except Quiz.DoesNotExist:
            return None

    def get_by_permalink(self, permalink: str) -> Optional[QuizEntity]:
        try:
            m = Quiz.objects.select_related('subject', 'course', 'created_by').get(permalink=permalink)
            return self._to_entity(m)
        except Quiz.DoesNotExist:
            return None

    def list_published(self, created_by_username: Optional[str] = None) -> List[QuizSummaryDTO]:
        qs = Quiz.objects.filter(status='published').select_related('subject', 'course', 'created_by')
        if created_by_username:
            qs = qs.filter(created_by__username=created_by_username)
        qs = qs.order_by('-created_at')

        return [
            QuizSummaryDTO(
                id=m.id,
                title=m.title,
                permalink=m.permalink,
                quiz_type=m.quiz_type,
                status=m.status,
                created_by_id=m.created_by_id,
                created_by_name=m.created_by.username if m.created_by else "",
                subject_id=m.subject_id,
                subject_name=m.subject.name if m.subject else None,
                course_id=m.course_id,
                course_title=m.course.title if m.course else None,
                attempt_count=m.attempt_count or 0,
                difficulty_level=m.difficulty_level,
                computed_difficulty_score=m.computed_difficulty_score
            )
            for m in qs
        ]

    def set_status(self, quiz_id: int, status: str) -> QuizEntity:
        m = Quiz.objects.get(id=quiz_id)
        m.status = status
        m.save(update_fields=['status'])
        return self._to_entity(m)

    @staticmethod
    def _to_entity(m: Quiz) -> QuizEntity:
        return QuizEntity(
            id=m.id,
            title=m.title,
            content=m.content,
            is_locked=m.is_locked,
            lesson_id=m.lesson_id,
            subject_id=m.subject_id,
            course_id=m.course_id,
            created_by_id=m.created_by_id,
            created_at=m.created_at,
            quiz_type=QuizType(m.quiz_type) if m.quiz_type in [e.value for e in QuizType] else QuizType.FREE,
            permalink=m.permalink,
            status=QuizStatus(m.status) if m.status in [e.value for e in QuizStatus] else QuizStatus.DRAFT,
            published_at=m.published_at,
            difficulty_level=DifficultyLevel(m.difficulty_level) if m.difficulty_level in [e.value for e in DifficultyLevel] else DifficultyLevel.MEDIUM,
            computed_difficulty_score=m.computed_difficulty_score,
            attempt_count=m.attempt_count or 0,
        )
