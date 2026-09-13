"""
Use Case: Get user profile details.
"""
from core.shared_kernel.domain.result import Result, ok, err
from users.application.dtos import UserProfileDTO
from users.application.ports.outbound.user_repository_port import UserRepositoryPort
from users.domain.exceptions import UserNotFoundError


class GetUserProfileUseCase:
    def __init__(self, user_repo: UserRepositoryPort):
        self._user_repo = user_repo

    def execute(self, user_id: int) -> Result[UserProfileDTO, Exception]:
        user = self._user_repo.get_by_id(user_id)
        if not user:
            return err(UserNotFoundError(str(user_id)))

        profile = self._user_repo.get_profile_by_user_id(user_id)
        if not profile:
            return err(UserNotFoundError(f"Profile for user {user_id}"))

        dto = UserProfileDTO(
            user_id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            display_name=profile.display_name or user.full_name,
            role=profile.role,
            bio=profile.bio or "",
            active_guide=profile.active_guide,
            is_staff=user.is_staff,
            date_joined=user.created_at.strftime("%Y-%m-%d") if user.created_at else "",
            growth_score=profile.growth_score,
            impact_score=profile.impact_score,
            teacher_tagline=profile.teacher_tagline,
            teacher_about=profile.teacher_about,
            teaching_specialties=profile.teaching_specialties,
        )
        return ok(dto)
