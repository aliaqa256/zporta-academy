"""
Django ORM implementation of UserRepositoryPort.
Maps between Django ORM models and pure domain entities.
"""
from typing import Optional, List, Tuple
from django.contrib.auth.models import User
from django.db.models import Q
from users.domain.entities import UserEntity, ProfileEntity, UserPreferenceEntity
from users.application.ports.outbound.user_repository_port import UserRepositoryPort
from users.models import Profile, UserPreference


class DjangoUserRepository(UserRepositoryPort):
    def _map_user_to_entity(self, user: User) -> UserEntity:
        return UserEntity(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_staff=user.is_staff,
            is_superuser=user.is_superuser,
            created_at=user.date_joined,
        )

    def _map_profile_to_entity(self, profile: Profile) -> ProfileEntity:
        return ProfileEntity(
            id=profile.id,
            user_id=profile.user_id,
            display_name=profile.display_name or "",
            role=profile.role,
            bio=profile.bio or "",
            active_guide=profile.active_guide,
            can_invite_teachers=profile.can_invite_teachers,
            growth_score=profile.growth_score,
            impact_score=profile.impact_score,
            teacher_tagline=profile.teacher_tagline,
            teacher_about=profile.teacher_about,
            teaching_specialties=profile.teaching_specialties,
        )

    def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        try:
            user = User.objects.get(id=user_id)
            return self._map_user_to_entity(user)
        except User.DoesNotExist:
            return None

    def get_by_username(self, username: str) -> Optional[UserEntity]:
        try:
            user = User.objects.get(username__iexact=username)
            return self._map_user_to_entity(user)
        except User.DoesNotExist:
            return None

    def get_by_email(self, email: str) -> Optional[UserEntity]:
        try:
            user = User.objects.get(email__iexact=email)
            return self._map_user_to_entity(user)
        except User.DoesNotExist:
            return None

    def find_by_credential(self, credential: str) -> Optional[UserEntity]:
        user = User.objects.filter(
            Q(username__iexact=credential) | Q(email__iexact=credential)
        ).first()
        return self._map_user_to_entity(user) if user else None

    def exists_by_username(self, username: str) -> bool:
        return User.objects.filter(username__iexact=username).exists()

    def exists_by_email(self, email: str) -> bool:
        return User.objects.filter(email__iexact=email).exists()

    def create_user_with_profile(
        self, username: str, email: str, password_hash: str, role: str, bio: str
    ) -> Tuple[UserEntity, ProfileEntity]:
        user = User(username=username, email=email, password=password_hash)
        user.save()

        # Update auto-created profile (or create if signal skipped)
        profile, _ = Profile.objects.get_or_create(
            user=user, defaults={"role": role, "bio": bio}
        )
        profile.role = role
        profile.bio = bio
        profile.save()

        return self._map_user_to_entity(user), self._map_profile_to_entity(profile)

    def get_profile_by_user_id(self, user_id: int) -> Optional[ProfileEntity]:
        try:
            profile = Profile.objects.get(user_id=user_id)
            return self._map_profile_to_entity(profile)
        except Profile.DoesNotExist:
            return None

    def save_profile(self, profile: ProfileEntity) -> ProfileEntity:
        orm_profile, _ = Profile.objects.get_or_create(user_id=profile.user_id)
        orm_profile.display_name = profile.display_name
        orm_profile.bio = profile.bio
        orm_profile.role = profile.role
        orm_profile.teacher_tagline = profile.teacher_tagline
        orm_profile.teacher_about = profile.teacher_about
        orm_profile.teaching_specialties = profile.teaching_specialties
        orm_profile.growth_score = profile.growth_score
        orm_profile.impact_score = profile.impact_score
        orm_profile.save()
        return self._map_profile_to_entity(orm_profile)

    def get_preferences(self, user_id: int) -> Optional[UserPreferenceEntity]:
        try:
            pref = UserPreference.objects.get(user_id=user_id)
            return UserPreferenceEntity(
                user_id=user_id,
                interested_subjects=list(pref.interested_subjects.values_list("id", flat=True)),
                languages_spoken=pref.languages_spoken or [],
                location=pref.location,
            )
        except UserPreference.DoesNotExist:
            return None
