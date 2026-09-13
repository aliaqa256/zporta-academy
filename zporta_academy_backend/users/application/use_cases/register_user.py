"""
Use Case: Register a new user with profile.
Pure orchestration, 100% testable with in-memory fakes.
"""
from core.shared_kernel.domain.result import Result, ok, err
from users.application.dtos import RegisterUserCommand
from users.application.ports.outbound.user_repository_port import UserRepositoryPort
from users.application.ports.outbound.auth_service_port import AuthServicePort
from users.domain.value_objects import EmailAddress, Username, UserRole
from users.domain.policies import PasswordPolicy
from users.domain.exceptions import (
    UsernameAlreadyTakenError,
    EmailAlreadyRegisteredError,
    InvalidPasswordError,
)


class RegisterUserUseCase:
    def __init__(self, user_repo: UserRepositoryPort, auth_service: AuthServicePort):
        self._user_repo = user_repo
        self._auth_service = auth_service

    def execute(self, cmd: RegisterUserCommand) -> Result[str, Exception]:
        # 1. Validate Email & Username value objects
        try:
            email_vo = EmailAddress(cmd.email)
            username_vo = Username(cmd.username)
        except ValueError as ve:
            return err(ve)

        # 2. Validate Password policy
        valid, msg = PasswordPolicy.validate(cmd.password)
        if not valid:
            return err(InvalidPasswordError(msg))

        # 3. Check uniqueness via repository ports
        if self._user_repo.exists_by_username(str(username_vo)):
            return err(UsernameAlreadyTakenError(str(username_vo)))

        if self._user_repo.exists_by_email(str(email_vo)):
            return err(EmailAlreadyRegisteredError(str(email_vo)))

        # 4. Hash password and persist
        role_vo = UserRole.from_string(cmd.role)
        password_hash = self._auth_service.hash_password(cmd.password)

        try:
            self._user_repo.create_user_with_profile(
                username=str(username_vo),
                email=str(email_vo),
                password_hash=password_hash,
                role=role_vo.value,
                bio=cmd.bio or "",
            )
            return ok("User registered successfully.")
        except Exception as e:
            return err(e)
