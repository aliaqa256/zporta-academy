"""
Check User Course Access Use Case.
"""
from enrollment.application.dtos.enrollment_dtos import AccessResultDTO, CheckAccessQuery
from enrollment.application.ports.outbound.enrollment_repository_port import EnrollmentRepositoryPort
from enrollment.domain.policies import EnrollmentAccessPolicy


class CheckUserAccessUseCase:
    """Use case to verify whether a user has access to a course."""

    def __init__(self, repository: EnrollmentRepositoryPort):
        self._repository = repository

    def execute(self, query: CheckAccessQuery) -> AccessResultDTO:
        if query.is_staff:
            return AccessResultDTO(has_access=True, reason="Staff administrative access grant.")

        enrollments = self._repository.list_user_enrollments(query.user_id)
        has_access = EnrollmentAccessPolicy.has_course_access(
            user_id=query.user_id,
            course_id=query.course_id,
            enrollments=enrollments,
            is_staff=query.is_staff,
        )

        reason = "Active enrollment found." if has_access else "No active enrollment for this course."
        return AccessResultDTO(has_access=has_access, reason=reason)
