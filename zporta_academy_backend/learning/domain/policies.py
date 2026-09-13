"""
Learning & Spaced Repetition Domain Policies.
"""
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Tuple
from learning.domain.entities import StudyItemEntity, UserNoteEntity
from learning.domain.value_objects import NotePrivacy, ReviewRating


class SpacedRepetitionPolicy:
    """SuperMemo-2 (SM-2) Spaced Repetition algorithm for memory retention."""

    MIN_EASE_FACTOR = 1.3

    @classmethod
    def calculate_next_schedule(
        cls,
        repetitions: int,
        ease_factor: float,
        interval_days: int,
        rating: ReviewRating,
        now: datetime = None,
    ) -> Tuple[int, float, int, datetime]:
        """
        Calculates (new_repetitions, new_ease_factor, new_interval_days, next_review_datetime).
        
        Quality mapping:
        - AGAIN: quality 1 (Failed recall - resets repetitions)
        - HARD: quality 3
        - GOOD: quality 4
        - EASY: quality 5
        """
        now = now or datetime.now(timezone.utc)

        quality_map = {
            ReviewRating.AGAIN: 1,
            ReviewRating.HARD: 3,
            ReviewRating.GOOD: 4,
            ReviewRating.EASY: 5,
        }
        q = quality_map.get(rating, 4)

        if q < 3:
            # Failure: reset repetition count, interval becomes 1 day
            new_repetitions = 0
            new_interval = 1
        else:
            # Success: increment repetition count
            new_repetitions = repetitions + 1
            if new_repetitions == 1:
                new_interval = 1
            elif new_repetitions == 2:
                new_interval = 6
            else:
                new_interval = max(1, round(interval_days * ease_factor))

        # Adjust ease factor: EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        delta_ef = 0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)
        new_ease = max(cls.MIN_EASE_FACTOR, ease_factor + delta_ef)

        next_due = now + timedelta(days=new_interval)
        return new_repetitions, round(new_ease, 2), new_interval, next_due


class StudyRecommendationPolicy:
    """Filters recommendations by subject interests and ensures diverse study queue."""

    @staticmethod
    def extract_subject_interest_ids(events: List[Dict[str, Any]]) -> List[int]:
        subject_ids = []
        for ev in events:
            sub_id = ev.get("subject_id")
            if sub_id and sub_id not in subject_ids:
                subject_ids.append(sub_id)
        return subject_ids


class NoteAccessPolicy:
    """Validates user permission to view or edit notes."""

    @staticmethod
    def can_view(note: UserNoteEntity, user_id: int, is_staff: bool = False) -> bool:
        if is_staff or note.user_id == user_id:
            return True
        if note.privacy == NotePrivacy.PUBLIC:
            return True
        if note.privacy == NotePrivacy.MENTION and user_id in note.mentions:
            return True
        return False

    @staticmethod
    def can_edit(note: UserNoteEntity, user_id: int, is_staff: bool = False) -> bool:
        if is_staff or note.user_id == user_id:
            return True
        return False
