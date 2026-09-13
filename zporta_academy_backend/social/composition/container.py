from social.application.ports.outbound.social_repository_port import SocialRepositoryPort
from social.application.use_cases.manage_guide_request import ManageGuideRequestUseCase
from social.adapters.outbound.persistence.django_social_repository import DjangoSocialRepository


def build_social_repository() -> SocialRepositoryPort:
    return DjangoSocialRepository()


def build_manage_guide_request_use_case(
    repository: SocialRepositoryPort = None
) -> ManageGuideRequestUseCase:
    return ManageGuideRequestUseCase(
        repository=repository or build_social_repository()
    )
