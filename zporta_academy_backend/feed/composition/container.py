from feed.application.ports.outbound.feed_repository_port import FeedRepositoryPort
from feed.application.use_cases.get_personalized_feed import GetPersonalizedFeedUseCase
from feed.adapters.outbound.persistence.django_feed_repository import DjangoFeedRepository


def build_feed_repository() -> FeedRepositoryPort:
    return DjangoFeedRepository()


def build_get_personalized_feed_use_case(
    repository: FeedRepositoryPort = None
) -> GetPersonalizedFeedUseCase:
    return GetPersonalizedFeedUseCase(
        repository=repository or build_feed_repository()
    )
