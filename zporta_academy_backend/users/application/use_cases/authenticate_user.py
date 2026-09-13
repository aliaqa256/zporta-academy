"""
Use Case: Authenticate user by username or email.
"""
from core.shared_kernel.domain.result import Result, ok, err
from users.application.dtos import AuthenticateUserCommand, AuthResultDTO
from users.application.ports.outbound.user_repository_port import UserRepositoryPort
from users.application.ports.outbound.auth_service_port import AuthServicePort
from users.domain.exceptions import InvalidCredentialsError, UserNotFoundError


class AuthenticateUserUseCase:
    def __init__(self, user_repo: UserRepositoryPort, auth_service: AuthServicePort):
        self._user_repo = user_repo
        self._auth_service = auth_service

    def execute(self, cmd: AuthenticateUserCommand) -> Result[AuthResultDTO, Exception]:
        if not cmd.credential or not cmd.password:
            return err(InvalidCredentialsError("Username/Email and password are required."))

        user_id = self._auth_service.authenticate_credential(cmd.credential, cmd.password)
        if not user_id:
            return err(InvalidCredentialsError("Invalid credentials."))

        user = self._user_repo.get_by_id(user_id)
        if not user:
            return err(UserNotFoundError(cmd.credential))

        profile = self._user_repo.get_profile_by_user_id(user.id)
        token = self._auth_service.get_or_create_token(user.id)
        pref = self._user_repo.get_preferences(user.id)

        preferences_data = {
            "languages_spoken": pref.languages_spoken if pref else [],
            "location": pref.location if pref else None,
            "bio": profile.bio if profile else None,
            "interested_tags": [],
        }

        result = AuthResultDTO(
            token=token,
            user_id=user.id,
            username=user.username,
            email=user.email,
            role=profile.role if profile else "explorer",
            active_guide=profile.active_guide if profile else False,
            locale="en",
            preferences=preferences_data,
        )
        return ok(result)
