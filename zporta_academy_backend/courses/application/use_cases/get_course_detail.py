"""
Use Case: Get course detail with access policy checks.
"""
from typing import Optional
from core.shared_kernel.domain.result import Result, ok, err
from courses.domain.policies import CourseAccessPolicy
from courses.domain.exceptions import CourseNotFoundError, CourseAccessDeniedError
from courses.application.dtos import CourseDetailDTO
from courses.application.ports.outbound.course_repository_port import CourseRepositoryPort


class GetCourseDetailUseCase:
    def __init__(self, course_repo: CourseRepositoryPort):
        self._course_repo = course_repo

    def execute(
        self,
        permalink: str,
        user_id: Optional[int] = None,
        is_staff: bool = False,
        is_superuser: bool = False
    ) -> Result[CourseDetailDTO, Exception]:
        course = self._course_repo.get_by_permalink(permalink)
        if not course:
            return err(CourseNotFoundError(permalink))

        can_view = CourseAccessPolicy.can_view_course(
            is_draft=course.is_draft,
            user_id=user_id,
            creator_id=course.created_by_id,
            allowed_tester_ids=course.allowed_tester_ids,
            is_staff=is_staff,
            is_superuser=is_superuser,
        )
        if not can_view:
            return err(CourseAccessDeniedError())

        dto = CourseDetailDTO(
            id=course.id,
            title=course.title,
            description=course.description,
            permalink=course.permalink,
            price=course.price,
            course_type=course.course_type,
            cover_image_url=course.cover_image_url,
            subject_id=course.subject_id,
            subject_name="",
            created_by_id=course.created_by_id,
            created_by_name="",
            lesson_count=0,
            is_draft=course.is_draft,
            is_locked=course.is_locked,
            is_owner=(user_id == course.created_by_id),
            canonical_url=f"/courses/{course.permalink}/",
        )
        return ok(dto)
