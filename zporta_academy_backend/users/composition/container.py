"""
Composition Root for Users Domain.
Constructs use cases with concrete adapters.
"""
from users.adapters.outbound.persistence.django_user_repository import DjangoUserRepository
from users.adapters.outbound.auth.django_auth_service import DjangoAuthService
from users.application.use_cases.register_user import RegisterUserUseCase
from users.application.use_cases.authenticate_user import AuthenticateUserUseCase
from users.application.use_cases.get_user_profile import GetUserProfileUseCase
from users.application.use_cases.update_user_profile import UpdateUserProfileUseCase


def build_user_repository() -> DjangoUserRepository:
    return DjangoUserRepository()


def build_auth_service() -> DjangoAuthService:
    return DjangoAuthService()


def build_register_user_use_case() -> RegisterUserUseCase:
    return RegisterUserUseCase(
        user_repo=build_user_repository(),
        auth_service=build_auth_service(),
    )


def build_authenticate_user_use_case() -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase(
        user_repo=build_user_repository(),
        auth_service=build_auth_service(),
    )


def build_get_user_profile_use_case() -> GetUserProfileUseCase:
    return GetUserProfileUseCase(
        user_repo=build_user_repository(),
    )


def build_update_user_profile_use_case() -> UpdateUserProfileUseCase:
    repo = build_user_repository()
    get_profile = GetUserProfileUseCase(user_repo=repo)
    return UpdateUserProfileUseCase(
        user_repo=repo,
        get_profile_use_case=get_profile,
    )
