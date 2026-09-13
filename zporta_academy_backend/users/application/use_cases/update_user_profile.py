"""
Use Case: Update user profile details.
"""
from core.shared_kernel.domain.result import Result, ok, err
from users.application.dtos import UpdateProfileCommand, UserProfileDTO
from users.application.ports.outbound.user_repository_port import UserRepositoryPort
from users.domain.exceptions import UserNotFoundError
from users.application.use_cases.get_user_profile import GetUserProfileUseCase


class UpdateUserProfileUseCase:
    def __init__(self, user_repo: UserRepositoryPort, get_profile_use_case: GetUserProfileUseCase):
        self._user_repo = user_repo
        self._get_profile_use_case = get_profile_use_case

    def execute(self, cmd: UpdateProfileCommand) -> Result[UserProfileDTO, Exception]:
        profile = self._user_repo.get_profile_by_user_id(cmd.user_id)
        if not profile:
            return err(UserNotFoundError(f"Profile for user {cmd.user_id}"))

        if cmd.display_name is not None:
            profile.display_name = cmd.display_name
        if cmd.bio is not None:
            profile.bio = cmd.bio
        if cmd.role is not None:
            profile.role = cmd.role
        if cmd.teacher_tagline is not None:
            profile.teacher_tagline = cmd.teacher_tagline
        if cmd.teacher_about is not None:
            profile.teacher_about = cmd.teacher_about
        if cmd.teaching_specialties is not None:
            profile.teaching_specialties = cmd.teaching_specialties

        self._user_repo.save_profile(profile)
        return self._get_profile_use_case.execute(cmd.user_id)
