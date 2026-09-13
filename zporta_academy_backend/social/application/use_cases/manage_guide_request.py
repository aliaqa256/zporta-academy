from social.domain.entities import GuideRequestStatus
from social.domain.policies import GuideRequestPolicy
from social.domain.exceptions import (
    GuideRequestNotFoundError,
    UnauthorizedSocialActionError,
)
from ..ports.outbound.social_repository_port import SocialRepositoryPort


class ManageGuideRequestUseCase:
    """Handles accepting, declining, and cancelling guide requests."""

    def __init__(self, repository: SocialRepositoryPort):
        self.repository = repository

    def cancel_request(self, request_id: int, user_id: int) -> None:
        entity = self.repository.get_guide_request_by_id(request_id)
        if not entity:
            raise GuideRequestNotFoundError(f"Guide request #{request_id} not found.")

        if not GuideRequestPolicy.can_cancel(entity, user_id):
            raise UnauthorizedSocialActionError("Only the requester can cancel this guide request.")

        self.repository.delete_guide_request(request_id)

    def respond_to_request(self, request_id: int, user_id: int, accept: bool) -> str:
        entity = self.repository.get_guide_request_by_id(request_id)
        if not entity:
            raise GuideRequestNotFoundError(f"Guide request #{request_id} not found.")

        if not GuideRequestPolicy.can_respond(entity, user_id):
            raise UnauthorizedSocialActionError("Only the target guide can respond to this request.")

        new_status = GuideRequestStatus.ACCEPTED.value if accept else GuideRequestStatus.DECLINED.value
        self.repository.update_request_status(request_id, new_status)
        return new_status
