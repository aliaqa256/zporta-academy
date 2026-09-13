"""
Use Cases: Publish lesson and List lessons.
"""
from typing import List
from core.shared_kernel.domain.result import Result, ok, err
from lessons.domain.entities import LessonEntity
from lessons.domain.policies import LessonPublishPolicy
from lessons.domain.exceptions import LessonNotFoundError, LessonAccessDeniedError, InvalidLessonStateError
from lessons.application.dtos import LessonFilterQueryDTO, LessonSummaryDTO
from lessons.application.ports.outbound.lesson_repository_port import LessonRepositoryPort


class PublishLessonUseCase:
    def __init__(self, lesson_repo: LessonRepositoryPort):
        self._lesson_repo = lesson_repo

    def execute(self, lesson_id: int, user_id: int, is_staff: bool = False) -> Result[LessonEntity, Exception]:
        lesson = self._lesson_repo.get_by_id(lesson_id)
        if not lesson:
            return err(LessonNotFoundError(str(lesson_id)))

        if lesson.created_by_id != user_id and not is_staff:
            return err(LessonAccessDeniedError("Only the lesson author or staff can publish this lesson."))

        # Enforce publish policy
        valid, msg = LessonPublishPolicy.validate_publishable(
            is_premium=lesson.is_premium,
            has_course=(lesson.course_id is not None),
            is_course_premium=True,
        )
        if not valid:
            return err(InvalidLessonStateError(msg))

        updated = self._lesson_repo.set_status(lesson_id, status="published")
        return ok(updated)


class ListLessonsUseCase:
    def __init__(self, lesson_repo: LessonRepositoryPort):
        self._lesson_repo = lesson_repo

    def execute(self, query: LessonFilterQueryDTO) -> Result[List[LessonSummaryDTO], Exception]:
        try:
            lessons = self._lesson_repo.list_lessons(query)
            return ok(lessons)
        except Exception as e:
            return err(e)
