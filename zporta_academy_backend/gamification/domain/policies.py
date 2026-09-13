from datetime import date, timedelta
from typing import List, Dict


class GamificationPointsPolicy:
    """Pure domain rules for awarding activity points."""

    POINTS_MAP: Dict[str, int] = {
        "correct_answer": 1,
        "lesson_completed": 5,
        "standalone_lesson": 3,
        "course_completed": 25,
        "enrollment_premium": 8,
        "enrollment_free": 4,
        "course_enrolled": 2,
        "quiz_first_attempt": 4,
    }

    @classmethod
    def get_points_for_activity(cls, activity_type: str) -> int:
        return cls.POINTS_MAP.get(activity_type, 0)


class StreakPolicy:
    """Pure domain calculation for daily learning streak continuity."""

    @staticmethod
    def calculate_current_streak(activity_dates: List[date], reference_date: date) -> int:
        if not activity_dates:
            return 0

        unique_dates = sorted(set(activity_dates), reverse=True)
        if not unique_dates:
            return 0

        # Check if latest activity was today or yesterday
        most_recent = unique_dates[0]
        if most_recent < reference_date - timedelta(days=1):
            return 0

        streak = 0
        expected = most_recent
        for d in unique_dates:
            if d == expected:
                streak += 1
                expected = d - timedelta(days=1)
            elif d < expected:
                break
        return streak
