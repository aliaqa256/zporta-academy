"""
Use Case: Get lesson detail with content gating policy evaluation.
"""
from typing import Optional
from core.shared_kernel.domain.result import Result, ok, err
from lessons.domain.policies import ContentGatingPolicy
from lessons.domain.exceptions import LessonNotFoundError, LessonAccessDeniedError
from lessons.application.dtos import LessonDetailDTO
from lessons.application.ports.outbound.lesson_repository_port import LessonRepositoryPort


class GetLessonDetailUseCase:
    def __init__(self, lesson_repo: LessonRepositoryPort):
        self._lesson_repo = lesson_repo

    def execute(
        self,
        permalink: str,
        user_id: Optional[int] = None,
        is_staff: bool = False,
        is_superuser: bool = False
    ) -> Result[LessonDetailDTO, Exception]:
        lesson = self._lesson_repo.get_by_permalink(permalink)
        if not lesson:
            return err(LessonNotFoundError(permalink))

        # Check draft visibility
        if not lesson.is_published:
            can_view_draft = (
                user_id is not None
                and (user_id == lesson.created_by_id or is_staff or is_superuser)
            )
            if not can_view_draft:
                return err(LessonAccessDeniedError("Draft lesson is only accessible to creator or staff."))

        # Check course enrollment for gating
        is_enrolled = False
        if user_id and lesson.course_id:
            is_enrolled = self._lesson_repo.is_user_enrolled_in_course(user_id, lesson.course_id)

        access_level = ContentGatingPolicy.evaluate_access(
            is_premium=lesson.is_premium,
            user_id=user_id,
            creator_id=lesson.created_by_id,
            is_enrolled=is_enrolled,
            is_staff=is_staff,
            is_superuser=is_superuser,
        )

        content, is_gated = ContentGatingPolicy.process_content(lesson.content, access_level)

        is_completed = False
        if user_id:
            is_completed = self._lesson_repo.is_lesson_completed_by_user(user_id, lesson.id)

        dto = LessonDetailDTO(
            id=lesson.id,
            title=lesson.title,
            content=content,
            permalink=lesson.permalink,
            video_url=lesson.video_url,
            subject_id=lesson.subject_id,
            subject_name="",
            course_id=lesson.course_id,
            course_title="",
            created_by_id=lesson.created_by_id,
            created_by_name="",
            status=lesson.status,
            is_premium=lesson.is_premium,
            is_locked=lesson.is_locked,
            is_gated=is_gated,
            is_completed=is_completed,
            is_owner=(user_id == lesson.created_by_id),
            position=lesson.position,
            canonical_url=f"/lessons/{lesson.permalink}/",
        )
        return ok(dto)
