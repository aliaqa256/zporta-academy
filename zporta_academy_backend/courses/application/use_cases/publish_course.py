"""
Use Cases: Publish and Unpublish courses.
"""
from core.shared_kernel.domain.result import Result, ok, err
from courses.domain.exceptions import CourseNotFoundError, CourseAccessDeniedError, CannotDraftEnrolledCourseError
from courses.domain.entities import CourseEntity
from courses.application.ports.outbound.course_repository_port import CourseRepositoryPort


class PublishCourseUseCase:
    def __init__(self, course_repo: CourseRepositoryPort):
        self._course_repo = course_repo

    def execute(self, course_id: int, user_id: int, is_staff: bool = False) -> Result[CourseEntity, Exception]:
        course = self._course_repo.get_by_id(course_id)
        if not course:
            return err(CourseNotFoundError(str(course_id)))

        if course.created_by_id != user_id and not is_staff:
            return err(CourseAccessDeniedError("Only the creator or staff can publish this course."))

        updated = self._course_repo.set_draft_status(course_id, is_draft=False)
        return ok(updated)


class UnpublishCourseUseCase:
    def __init__(self, course_repo: CourseRepositoryPort):
        self._course_repo = course_repo

    def execute(self, course_id: int, user_id: int, is_staff: bool = False) -> Result[CourseEntity, Exception]:
        course = self._course_repo.get_by_id(course_id)
        if not course:
            return err(CourseNotFoundError(str(course_id)))

        if course.created_by_id != user_id and not is_staff:
            return err(CourseAccessDeniedError("Only the creator or staff can unpublish this course."))

        if self._course_repo.has_active_enrollments(course_id):
            return err(CannotDraftEnrolledCourseError())

        updated = self._course_repo.set_draft_status(course_id, is_draft=True)
        return ok(updated)
