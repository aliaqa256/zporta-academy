from typing import Optional, List
from django.contrib.auth import get_user_model
from social.domain.entities import (
    GuideRequestEntity,
    GuideRequestStatus,
    ConnectedUserCardEntity,
)
from social.application.ports.outbound.social_repository_port import SocialRepositoryPort
from social.models import GuideRequest

User = get_user_model()


class DjangoSocialRepository(SocialRepositoryPort):
    """Django ORM implementation of SocialRepositoryPort."""

    def get_guide_request_by_id(self, request_id: int) -> Optional[GuideRequestEntity]:
        try:
            gr = GuideRequest.objects.get(id=request_id)
            return GuideRequestEntity(
                id=gr.id,
                explorer_id=gr.explorer_id,
                guide_id=gr.guide_id,
                status=GuideRequestStatus(gr.status),
                created_at=gr.created_at
            )
        except GuideRequest.DoesNotExist:
            return None

    def update_request_status(self, request_id: int, status: str) -> None:
        GuideRequest.objects.filter(id=request_id).update(status=status)

    def delete_guide_request(self, request_id: int) -> None:
        GuideRequest.objects.filter(id=request_id).delete()

    def get_user_teachers(self, user_id: int) -> List[ConnectedUserCardEntity]:
        requests = GuideRequest.objects.filter(
            explorer_id=user_id,
            status='accepted'
        ).select_related('guide', 'guide__profile')

        results = []
        for gr in requests:
            t = gr.guide
            profile = getattr(t, 'profile', None)
            display = profile.display_name if profile and profile.display_name else t.username
            pic_url = profile.profile_image.url if profile and profile.profile_image else None
            results.append(ConnectedUserCardEntity(
                id=t.id,
                username=t.username,
                display_name=display,
                profile_picture_url=pic_url
            ))
        return results

    def get_user_students(self, teacher_id: int) -> List[ConnectedUserCardEntity]:
        requests = GuideRequest.objects.filter(
            guide_id=teacher_id,
            status='accepted'
        ).select_related('explorer', 'explorer__profile')

        results = []
        for gr in requests:
            s = gr.explorer
            profile = getattr(s, 'profile', None)
            display = profile.display_name if profile and profile.display_name else s.username
            pic_url = profile.profile_image.url if profile and profile.profile_image else None
            results.append(ConnectedUserCardEntity(
                id=s.id,
                username=s.username,
                display_name=display,
                profile_picture_url=pic_url
            ))
        return results
