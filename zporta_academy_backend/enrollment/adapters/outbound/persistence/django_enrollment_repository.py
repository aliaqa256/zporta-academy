"""
Django Enrollment Repository Persistence Adapter.
"""
from typing import List, Optional
from django.contrib.contenttypes.models import ContentType
from courses.models import Course
from enrollment.application.ports.outbound.enrollment_repository_port import EnrollmentRepositoryPort
from enrollment.domain.entities import EnrollmentEntity, ShareInviteEntity
from enrollment.domain.value_objects import EnrollmentStatus, EnrollmentType
from enrollment.models import Enrollment, ShareInvite


class DjangoEnrollmentRepository(EnrollmentRepositoryPort):
    """PostgreSQL / SQLite persistence adapter for Enrollment and ShareInvite."""

    def _to_entity(self, model: Enrollment) -> EnrollmentEntity:
        return EnrollmentEntity(
            id=model.id,
            user_id=model.user_id,
            username=model.user.username if model.user else "",
            content_type_id=model.content_type_id,
            content_type_name=model.content_type.model if model.content_type else "course",
            object_id=model.object_id,
            content_title=str(model.content_object) if model.content_object else f"Item {model.object_id}",
            status=EnrollmentStatus(model.status) if model.status in EnrollmentStatus._value2member_map_ else EnrollmentStatus.ACTIVE,
            enrollment_type=EnrollmentType(model.enrollment_type) if model.enrollment_type in EnrollmentType._value2member_map_ else EnrollmentType.COURSE,
            enrollment_date=model.enrollment_date,
        )

    def get_by_id(self, enrollment_id: int) -> Optional[EnrollmentEntity]:
        try:
            m = Enrollment.objects.select_related("user", "content_type").get(pk=enrollment_id)
            return self._to_entity(m)
        except Enrollment.DoesNotExist:
            return None

    def find_enrollment(self, user_id: int, object_id: int, enrollment_type: str = "course") -> Optional[EnrollmentEntity]:
        qs = Enrollment.objects.filter(user_id=user_id, object_id=object_id, enrollment_type=enrollment_type).select_related("user", "content_type")
        m = qs.first()
        return self._to_entity(m) if m else None

    def list_user_enrollments(self, user_id: int) -> List[EnrollmentEntity]:
        qs = Enrollment.objects.filter(user_id=user_id).select_related("user", "content_type").order_by("-enrollment_date")
        return [self._to_entity(m) for m in qs]

    def list_course_enrollments(self, course_id: int) -> List[EnrollmentEntity]:
        course_ct = ContentType.objects.get_for_model(Course)
        qs = Enrollment.objects.filter(content_type=course_ct, object_id=course_id).select_related("user", "content_type").order_by("-enrollment_date")
        return [self._to_entity(m) for m in qs]

    def save(self, enrollment: EnrollmentEntity) -> EnrollmentEntity:
        course_ct = ContentType.objects.get_for_model(Course)
        content_type_id = enrollment.content_type_id or course_ct.id

        if enrollment.id:
            model = Enrollment.objects.get(pk=enrollment.id)
        else:
            model = Enrollment(
                user_id=enrollment.user_id,
                content_type_id=content_type_id,
                object_id=enrollment.object_id,
            )

        model.status = enrollment.status.value
        model.enrollment_type = enrollment.enrollment_type.value
        model.save()
        return self._to_entity(model)

    def find_invite_by_token(self, token: str) -> Optional[ShareInviteEntity]:
        try:
            invite = ShareInvite.objects.get(token=token)
            return ShareInviteEntity(
                id=invite.id,
                enrollment_id=invite.enrollment_id,
                invited_user_id=invite.invited_user_id,
                invited_by_id=invite.invited_by_id,
                token=invite.token,
                created_at=invite.created_at,
            )
        except ShareInvite.DoesNotExist:
            return None
