"""
Enroll User in Course Use Case.
"""
from datetime import datetime, timezone
from enrollment.application.dtos.enrollment_dtos import EnrollUserCommand, EnrollmentDTO
from enrollment.application.ports.outbound.enrollment_repository_port import EnrollmentRepositoryPort
from enrollment.domain.entities import EnrollmentEntity
from enrollment.domain.exceptions import AlreadyEnrolledError
from enrollment.domain.policies import EnrollmentAccessPolicy
from enrollment.domain.value_objects import EnrollmentStatus, EnrollmentType


class EnrollUserInCourseUseCase:
    """Use case to enroll a user in a course or learning item."""

    def __init__(self, repository: EnrollmentRepositoryPort):
        self._repository = repository

    def execute(self, cmd: EnrollUserCommand) -> EnrollmentDTO:
        existing = self._repository.find_enrollment(
            user_id=cmd.user_id,
            object_id=cmd.object_id,
            enrollment_type=cmd.enrollment_type,
        )

        if not EnrollmentAccessPolicy.can_enroll(cmd.user_id, cmd.object_id, existing):
            raise AlreadyEnrolledError(
                f"User {cmd.user_id} is already actively enrolled in {cmd.enrollment_type} {cmd.object_id}."
            )

        status_enum = EnrollmentStatus(cmd.status) if cmd.status in EnrollmentStatus._value2member_map_ else EnrollmentStatus.ACTIVE
        type_enum = EnrollmentType(cmd.enrollment_type) if cmd.enrollment_type in EnrollmentType._value2member_map_ else EnrollmentType.COURSE

        entity = EnrollmentEntity(
            id=existing.id if existing else None,
            user_id=cmd.user_id,
            object_id=cmd.object_id,
            status=status_enum,
            enrollment_type=type_enum,
            enrollment_date=datetime.now(timezone.utc),
        )

        saved = self._repository.save(entity)

        return EnrollmentDTO(
            id=saved.id or 0,
            user_id=saved.user_id,
            username=saved.username,
            object_id=saved.object_id,
            content_title=saved.content_title,
            enrollment_type=saved.enrollment_type.value,
            status=saved.status.value,
            enrollment_date=saved.enrollment_date,
        )
