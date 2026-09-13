"""
Django DailyCast Repository Adapter.
"""
import logging
import time
from datetime import timedelta
from typing import Any, Dict, List, Optional
from django.core.files.base import ContentFile
from django.utils import timezone
from dailycast.application.ports.outbound.dailycast_repository_port import DailyCastRepositoryPort
from dailycast.domain.entities import DailyPodcastEntity
from dailycast.domain.value_objects import MonthRange, OutputFormat, PodcastStatus, ReplySize
from dailycast.models import DailyPodcast

logger = logging.getLogger(__name__)


class DjangoDailyCastRepository(DailyCastRepositoryPort):
    """PostgreSQL / SQLite persistence adapter for DailyPodcast."""

    def _to_entity(self, model: DailyPodcast) -> DailyPodcastEntity:
        return DailyPodcastEntity(
            id=model.id,
            user_id=model.user_id,
            primary_language=model.primary_language,
            secondary_language=model.secondary_language or "",
            output_format=OutputFormat(model.output_format) if model.output_format in OutputFormat._value2member_map_ else OutputFormat.BOTH,
            month_range=MonthRange(model.month_range) if model.month_range in MonthRange._value2member_map_ else MonthRange.CURRENT,
            reply_size=ReplySize(model.reply_size) if model.reply_size in ReplySize._value2member_map_ else ReplySize.MEDIUM,
            included_courses=model.included_courses or [],
            category=model.category or "",
            topic=model.topic or "",
            profession=model.profession or "",
            notes=model.notes or "",
            request_data=model.request_data or {},
            script_text=model.script_text or "",
            questions_asked=model.questions_asked or [],
            student_answers=model.student_answers or {},
            audio_file_url=model.audio_file.url if model.audio_file else None,
            audio_file_secondary_url=model.audio_file_secondary.url if model.audio_file_secondary else None,
            llm_provider=model.llm_provider,
            tts_provider=model.tts_provider,
            duration_seconds=model.duration_seconds,
            duration_seconds_secondary=model.duration_seconds_secondary,
            status=PodcastStatus(model.status) if model.status in PodcastStatus._value2member_map_ else PodcastStatus.PENDING,
            error_message=model.error_message,
            requested_by_user=model.requested_by_user,
            requested_by_id=model.requested_by_id,
            user_request_type=model.user_request_type,
            can_request_again_at=model.can_request_again_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def get_by_id(self, podcast_id: int) -> Optional[DailyPodcastEntity]:
        try:
            model = DailyPodcast.objects.select_related("user").get(pk=podcast_id)
            return self._to_entity(model)
        except DailyPodcast.DoesNotExist:
            return None

    def list_for_user(self, user_id: int, is_staff: bool = False) -> List[DailyPodcastEntity]:
        qs = DailyPodcast.objects.all() if is_staff else DailyPodcast.objects.filter(user_id=user_id)
        return [self._to_entity(m) for m in qs.order_by("-created_at")]

    def save(
        self,
        podcast: DailyPodcastEntity,
        audio_bytes: Optional[bytes] = None,
        audio_bytes_secondary: Optional[bytes] = None,
    ) -> DailyPodcastEntity:
        if podcast.id:
            model = DailyPodcast.objects.get(pk=podcast.id)
        else:
            model = DailyPodcast(user_id=podcast.user_id)

        model.primary_language = podcast.primary_language
        model.secondary_language = podcast.secondary_language
        model.output_format = podcast.output_format.value
        model.month_range = podcast.month_range.value
        model.reply_size = podcast.reply_size.value
        model.included_courses = podcast.included_courses
        model.category = podcast.category
        model.topic = podcast.topic
        model.profession = podcast.profession
        model.notes = podcast.notes
        model.request_data = podcast.request_data
        model.script_text = podcast.script_text
        model.questions_asked = podcast.questions_asked
        model.student_answers = podcast.student_answers
        model.llm_provider = podcast.llm_provider
        model.tts_provider = podcast.tts_provider
        model.duration_seconds = podcast.duration_seconds
        model.duration_seconds_secondary = podcast.duration_seconds_secondary
        model.status = podcast.status.value
        model.error_message = podcast.error_message
        model.requested_by_user = podcast.requested_by_user
        model.requested_by_id = podcast.requested_by_id
        model.user_request_type = podcast.user_request_type
        model.can_request_again_at = podcast.can_request_again_at

        if audio_bytes:
            filename = f"podcast_{model.user_id}_{int(time.time())}.mp3"
            model.audio_file.save(filename, ContentFile(audio_bytes), save=False)

        if audio_bytes_secondary:
            filename_sec = f"podcast_{model.user_id}_{int(time.time())}_secondary.mp3"
            model.audio_file_secondary.save(filename_sec, ContentFile(audio_bytes_secondary), save=False)

        model.save()
        return self._to_entity(model)

    def check_recent_podcast_within_hours(self, user_id: int, hours: int = 24) -> Optional[DailyPodcastEntity]:
        cutoff = timezone.now() - timedelta(hours=hours)
        recent = (
            DailyPodcast.objects.filter(
                user_id=user_id,
                status=DailyPodcast.STATUS_COMPLETED,
                created_at__gte=cutoff,
            )
            .order_by("-created_at")
            .first()
        )
        return self._to_entity(recent) if recent else None

    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Aggregate user learning stats for podcast generation."""
        stats: Dict[str, Any] = {
            "ability_score": None,
            "ability_level": None,
            "weak_subject": None,
            "recent_quiz": None,
            "enrolled_courses": [],
            "notes_count": 0,
            "lessons_completed": 0,
            "quizzes_completed": 0,
            "time_spent_minutes": 0,
            "username": f"User {user_id}",
        }

        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            user = User.objects.get(pk=user_id)
            stats["username"] = user.username
        except User.DoesNotExist:
            return stats

        # Abilities
        try:
            from intelligence.models import UserAbilityProfile
            ability = UserAbilityProfile.objects.filter(user=user).first()
            if ability:
                stats["ability_score"] = ability.overall_ability_score
                stats["ability_level"] = ability.get_ability_level() if hasattr(ability, "get_ability_level") else "Intermediate"
                if ability.ability_by_subject:
                    weakest = min(ability.ability_by_subject.items(), key=lambda kv: kv[1])
                    stats["weak_subject"] = weakest[0]
        except Exception as e:
            logger.debug(f"UserAbility lookup skipped: {e}")

        # Enrolled courses
        try:
            from courses.models import Course
            from enrollment.models import Enrollment
            from django.contrib.contenttypes.models import ContentType
            course_type = ContentType.objects.get_for_model(Course)
            enrollments = Enrollment.objects.filter(
                user=user,
                content_type=course_type,
                enrollment_type="course",
            )
            stats["enrolled_courses"] = [
                {
                    "id": e.object_id,
                    "title": e.content_object.title if e.content_object else f"Course {e.object_id}",
                    "subject": getattr(e.content_object, "subject", "Unknown") if e.content_object else "Unknown",
                }
                for e in enrollments
                if e.content_object
            ]
        except Exception as e:
            logger.debug(f"Course enrollment lookup skipped: {e}")

        # Activity & time spent
        try:
            from learning.models import ActivityEvent
            events = ActivityEvent.objects.filter(user=user, event_type="podcast_interaction")
            stats["time_spent_minutes"] = sum(e.duration_seconds or 0 for e in events) // 60
        except Exception:
            pass

        return stats
