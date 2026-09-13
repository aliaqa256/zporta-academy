"""
Django ORM implementations of Intelligence repository ports.
"""
from typing import Optional, List
from django.contrib.contenttypes.models import ContentType
from intelligence.models import UserAbilityProfile, ContentDifficultyProfile, MatchScore
from intelligence.domain.entities import UserAbilityEntity, ContentDifficultyEntity, MatchScoreEntity
from intelligence.application.ports.outbound.ability_repository_port import AbilityRepositoryPort
from intelligence.application.ports.outbound.difficulty_repository_port import DifficultyRepositoryPort
from intelligence.application.ports.outbound.match_score_repository_port import MatchScoreRepositoryPort


class DjangoAbilityRepository(AbilityRepositoryPort):
    def get_by_user_id(self, user_id: int) -> Optional[UserAbilityEntity]:
        try:
            m = UserAbilityProfile.objects.select_related('user').get(user_id=user_id)
            return self._to_entity(m)
        except UserAbilityProfile.DoesNotExist:
            return None

    def save(self, profile: UserAbilityEntity) -> UserAbilityEntity:
        m, _ = UserAbilityProfile.objects.update_or_create(
            user_id=profile.user_id,
            defaults={
                'overall_ability_score': profile.overall_ability_score,
                'ability_by_subject': profile.ability_by_subject,
                'ability_by_tag': profile.ability_by_tag,
                'total_quizzes_attempted': profile.total_quizzes_attempted,
                'total_correct_answers': profile.total_correct_answers,
                'recent_performance_trend': profile.recent_performance_trend,
                'global_rank': profile.global_rank,
                'percentile': profile.percentile,
                'metadata': profile.metadata,
            }
        )
        return self._to_entity(m)

    def list_top_users(self, limit: int = 100) -> List[UserAbilityEntity]:
        qs = UserAbilityProfile.objects.select_related('user').order_by('-overall_ability_score')[:limit]
        return [self._to_entity(m) for m in qs]

    @staticmethod
    def _to_entity(m: UserAbilityProfile) -> UserAbilityEntity:
        return UserAbilityEntity(
            id=m.id,
            user_id=m.user_id,
            username=m.user.username if m.user else "",
            overall_ability_score=m.overall_ability_score,
            ability_by_subject=m.ability_by_subject or {},
            ability_by_tag=m.ability_by_tag or {},
            total_quizzes_attempted=m.total_quizzes_attempted,
            total_correct_answers=m.total_correct_answers,
            recent_performance_trend=m.recent_performance_trend,
            global_rank=m.global_rank,
            percentile=m.percentile,
            last_computed_at=m.last_computed_at,
            metadata=m.metadata or {}
        )


class DjangoDifficultyRepository(DifficultyRepositoryPort):
    def get_by_content(self, content_type_str: str, object_id: int) -> Optional[ContentDifficultyEntity]:
        try:
            ct = ContentType.objects.get(model=content_type_str.lower())
            m = ContentDifficultyProfile.objects.get(content_type=ct, object_id=object_id)
            return self._to_entity(m)
        except (ContentType.DoesNotExist, ContentDifficultyProfile.DoesNotExist):
            return None

    def save(self, profile: ContentDifficultyEntity) -> ContentDifficultyEntity:
        ct = ContentType.objects.get(model=profile.content_type.lower())
        m, _ = ContentDifficultyProfile.objects.update_or_create(
            content_type=ct,
            object_id=profile.object_id,
            defaults={
                'computed_difficulty_score': profile.computed_difficulty_score,
                'avg_time_spent_seconds': profile.avg_time_spent_seconds,
                'success_rate': profile.success_rate,
                'attempt_count': profile.attempt_count,
                'difficulty_by_user_segment': profile.difficulty_by_user_segment,
                'metadata': profile.metadata,
            }
        )
        return self._to_entity(m)

    def list_difficulties_for_ids(self, content_type_str: str, object_ids: List[int]) -> List[ContentDifficultyEntity]:
        try:
            ct = ContentType.objects.get(model=content_type_str.lower())
            qs = ContentDifficultyProfile.objects.filter(content_type=ct, object_id__in=object_ids)
            return [self._to_entity(m) for m in qs]
        except ContentType.DoesNotExist:
            return []

    @staticmethod
    def _to_entity(m: ContentDifficultyProfile) -> ContentDifficultyEntity:
        return ContentDifficultyEntity(
            id=m.id,
            content_type=m.content_type.model,
            object_id=m.object_id,
            computed_difficulty_score=m.computed_difficulty_score,
            avg_time_spent_seconds=m.avg_time_spent_seconds,
            success_rate=m.success_rate,
            attempt_count=m.attempt_count,
            difficulty_by_user_segment=m.difficulty_by_user_segment or {},
            last_computed_at=m.last_computed_at,
            metadata=m.metadata or {}
        )


class DjangoMatchScoreRepository(MatchScoreRepositoryPort):
    def get_top_matches_for_user(
        self,
        user_id: int,
        content_type_str: str = "quiz",
        limit: int = 20
    ) -> List[MatchScoreEntity]:
        try:
            ct = ContentType.objects.get(model=content_type_str.lower())
            qs = MatchScore.objects.filter(user_id=user_id, content_type=ct).order_by('-match_score')[:limit]
            return [self._to_entity(m) for m in qs]
        except ContentType.DoesNotExist:
            return []

    def save_match_scores(self, match_scores: List[MatchScoreEntity]) -> None:
        for ms in match_scores:
            ct = ContentType.objects.get(model=ms.content_type.lower())
            MatchScore.objects.update_or_create(
                user_id=ms.user_id,
                content_type=ct,
                object_id=ms.object_id,
                defaults={
                    'match_score': ms.match_score,
                    'difficulty_gap': ms.difficulty_gap,
                    'zpd_score': ms.zpd_score,
                    'preference_alignment_score': ms.preference_alignment_score,
                    'topic_similarity_score': ms.topic_similarity_score,
                    'recency_penalty': ms.recency_penalty,
                    'metadata': ms.metadata
                }
            )

    @staticmethod
    def _to_entity(m: MatchScore) -> MatchScoreEntity:
        return MatchScoreEntity(
            id=m.id,
            user_id=m.user_id,
            content_type=m.content_type.model,
            object_id=m.object_id,
            match_score=m.match_score,
            difficulty_gap=m.difficulty_gap,
            zpd_score=m.zpd_score,
            preference_alignment_score=m.preference_alignment_score,
            topic_similarity_score=m.topic_similarity_score,
            recency_penalty=m.recency_penalty,
            computed_at=m.computed_at,
            metadata=m.metadata or {}
        )
