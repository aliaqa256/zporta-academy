from abc import ABC, abstractmethod
from typing import Optional, List
from social.domain.entities import GuideRequestEntity, ConnectedUserCardEntity


class SocialRepositoryPort(ABC):
    """Abstract port for social relationships and guide requests."""

    @abstractmethod
    def get_guide_request_by_id(self, request_id: int) -> Optional[GuideRequestEntity]:
        pass

    @abstractmethod
    def update_request_status(self, request_id: int, status: str) -> None:
        pass

    @abstractmethod
    def delete_guide_request(self, request_id: int) -> None:
        pass

    @abstractmethod
    def get_user_teachers(self, user_id: int) -> List[ConnectedUserCardEntity]:
        pass

    @abstractmethod
    def get_user_students(self, teacher_id: int) -> List[ConnectedUserCardEntity]:
        pass
