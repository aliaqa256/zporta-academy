from datetime import date
from typing import Optional, List
from django.db import IntegrityError, models
from django.utils import timezone
from gamification.domain.entities import ActivityEntity, UserScoreEntity
from gamification.application.ports.outbound.gamification_repository_port import GamificationRepositoryPort
from gamification.models import Activity, UserScore, ActivityType


class DjangoGamificationRepository(GamificationRepositoryPort):
    """Django ORM implementation of GamificationRepositoryPort."""

    def log_activity(
        self,
        user_id: int,
        activity_type: str,
        points: int,
        unique_key: str,
        is_mistake: bool = False,
        metadata: dict = None,
        time_spent_seconds: Optional[int] = None
    ) -> Optional[ActivityEntity]:
        try:
            act = Activity.objects.create(
                user_id=user_id,
                activity_type=activity_type,
                points=points,
                unique_key=unique_key,
                is_mistake=is_mistake,
                metadata=metadata or {},
                time_spent_seconds=time_spent_seconds,
            )
            return ActivityEntity(
                id=act.id,
                user_id=act.user_id,
                activity_type=act.activity_type,
                points=act.points,
                unique_key=act.unique_key,
                is_mistake=act.is_mistake,
                metadata=act.metadata,
                time_spent_seconds=act.time_spent_seconds,
                created_at=act.created_at
            )
        except IntegrityError:
            # Activity with this unique key already logged
            return None

    def get_or_create_user_score(self, user_id: int) -> UserScoreEntity:
        score_obj, _ = UserScore.objects.get_or_create(user_id=user_id)
        return UserScoreEntity(
            user_id=score_obj.user_id,
            total_points=score_obj.total_points,
            lessons_completed=score_obj.lessons_completed,
            courses_completed=score_obj.courses_completed,
            correct_answers=score_obj.correct_answers,
            last_calculated=score_obj.last_calculated
        )

    def recalculate_user_score(self, user_id: int) -> UserScoreEntity:
        score_obj, _ = UserScore.objects.get_or_create(user_id=user_id)
        score_obj.recalculate()
        return UserScoreEntity(
            user_id=score_obj.user_id,
            total_points=score_obj.total_points,
            lessons_completed=score_obj.lessons_completed,
            courses_completed=score_obj.courses_completed,
            correct_answers=score_obj.correct_answers,
            last_calculated=score_obj.last_calculated
        )

    def get_user_activity_dates(self, user_id: int, days_limit: int = 365) -> List[date]:
        since = timezone.now() - timezone.timedelta(days=days_limit)
        dates = Activity.objects.filter(
            user_id=user_id,
            created_at__gte=since
        ).values_list('created_at', flat=True)
        return [d.date() for d in dates if d]
