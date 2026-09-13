"""
Enrollment Composition Container.
"""
from enrollment.adapters.outbound.persistence.django_enrollment_repository import DjangoEnrollmentRepository
from enrollment.application.ports.outbound.enrollment_repository_port import EnrollmentRepositoryPort
from enrollment.application.use_cases.check_user_access import CheckUserAccessUseCase
from enrollment.application.use_cases.enroll_user import EnrollUserInCourseUseCase


def build_enrollment_repository() -> EnrollmentRepositoryPort:
    return DjangoEnrollmentRepository()


def build_enroll_user_use_case(
    repository: EnrollmentRepositoryPort = None,
) -> EnrollUserInCourseUseCase:
    return EnrollUserInCourseUseCase(
        repository=repository or build_enrollment_repository()
    )


def build_check_user_access_use_case(
    repository: EnrollmentRepositoryPort = None,
) -> CheckUserAccessUseCase:
    return CheckUserAccessUseCase(
        repository=repository or build_enrollment_repository()
    )
