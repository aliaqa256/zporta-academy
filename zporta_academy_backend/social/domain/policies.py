from .entities import GuideRequestEntity, GuideRequestStatus


class GuideRequestPolicy:
    """Pure domain rules for guide requests."""

    @staticmethod
    def can_cancel(request_entity: GuideRequestEntity, user_id: int) -> bool:
        """Only the explorer who sent the request can cancel it."""
        return request_entity.explorer_id == user_id

    @staticmethod
    def can_respond(request_entity: GuideRequestEntity, user_id: int) -> bool:
        """Only the target guide can accept or decline."""
        return request_entity.guide_id == user_id and request_entity.status == GuideRequestStatus.PENDING
