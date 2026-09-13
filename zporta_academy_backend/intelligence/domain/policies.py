"""
Pure domain policies for ELO calculations, ZPD match scoring, and difficulty classification.
Zero framework dependencies.
"""
import math
from typing import Tuple, List, Optional
from .value_objects import EloScore, AbilityLevel, DifficultyTier


class EloCalculationPolicy:
    """Calculates ELO expected scores and rating adjustments."""

    DEFAULT_K_FACTOR = 32.0
    ESTABLISHED_K_FACTOR = 16.0
    SCALING_FACTOR = 400.0

    @classmethod
    def calculate_expected_score(cls, ability_rating: float, content_difficulty: float) -> float:
        """
        Calculates expected probability of success (0.0 to 1.0).
        E = 1 / (1 + 10^((D - A) / 400))
        """
        diff_exponent = (content_difficulty - ability_rating) / cls.SCALING_FACTOR
        # Guard against math overflow
        diff_exponent = max(-10.0, min(10.0, diff_exponent))
        return 1.0 / (1.0 + math.pow(10.0, diff_exponent))

    @classmethod
    def update_rating(
        cls,
        current_rating: float,
        content_difficulty: float,
        actual_score: float,
        attempts_count: int = 0
    ) -> float:
        """
        Calculates new rating after an attempt.
        actual_score: 1.0 for correct, 0.0 for incorrect.
        """
        k = cls.DEFAULT_K_FACTOR if attempts_count < 30 else cls.ESTABLISHED_K_FACTOR
        expected = cls.calculate_expected_score(current_rating, content_difficulty)
        delta = k * (actual_score - expected)
        new_rating = current_rating + delta
        # Clamp to 0..1000 scale
        return max(0.0, min(1000.0, new_rating))


class DifficultyClassificationPolicy:
    """Classifies scores into human-readable 5-tier and 4-tier bands."""

    @staticmethod
    def classify_5_tier(score: float) -> Tuple[DifficultyTier, str, str]:
        """Returns (tier_enum, label, color_code)."""
        if score < 320:
            return DifficultyTier.BEGINNER, "Beginner", "#22c55e"  # Green
        elif score < 420:
            return DifficultyTier.BEGINNER_MEDIUM, "Beginner → Medium", "#eab308"  # Yellow
        elif score < 520:
            return DifficultyTier.MEDIUM, "Medium", "#f97316"  # Orange
        elif score < 620:
            return DifficultyTier.MEDIUM_HARD, "Medium → Hard", "#ea580c"  # Dark Orange
        else:
            return DifficultyTier.HARD, "Hard / Expert", "#ef4444"  # Red

    @staticmethod
    def classify_ability_level(score: float, total_attempts: int = 0) -> str:
        if total_attempts == 0:
            return "Unranked"
        if score < 300:
            return "Beginner"
        elif score < 500:
            return "Intermediate"
        elif score < 700:
            return "Advanced"
        else:
            return "Expert"


class ZpdMatchScoringPolicy:
    """Calculates Zone of Proximal Development match scores (0-100 scale)."""

    @staticmethod
    def calculate_difficulty_gap(content_difficulty: float, user_ability: float) -> float:
        return content_difficulty - user_ability

    @staticmethod
    def calculate_zpd_score(difficulty_gap: float) -> float:
        """
        ZPD score is highest (1.0) when content is slightly challenging (+10 to +30 points above user),
        and drops off as content becomes too easy (<-50) or too hard (>+100).
        """
        # Gaussian centered at +20 gap with sigma=40
        optimal_gap = 20.0
        sigma = 40.0
        exponent = -((difficulty_gap - optimal_gap) ** 2) / (2 * (sigma ** 2))
        return math.exp(exponent)

    @classmethod
    def calculate_total_match_score(
        cls,
        difficulty_gap: float,
        preference_alignment: float = 1.0,
        topic_similarity: float = 1.0,
        recency_penalty: float = 0.0
    ) -> Tuple[float, float, str]:
        """
        Returns (match_score: 0-100, zpd_score: 0-1, why_explanation: str).
        """
        zpd = cls.calculate_zpd_score(difficulty_gap)
        
        # Weighted composite: 50% ZPD, 30% Preferences, 20% Topic - Recency
        raw_score = (
            (zpd * 50.0) +
            (preference_alignment * 30.0) +
            (topic_similarity * 20.0) -
            (recency_penalty * 40.0)
        )
        match_score = max(0.0, min(100.0, raw_score))

        # Generate human-readable explanation
        explanations = []
        if zpd > 0.7:
            if -50 <= difficulty_gap <= 50:
                explanations.append("Perfect difficulty for your level 🎯")
            elif difficulty_gap > 50:
                explanations.append("Challenge yourself! 🚀")
            elif difficulty_gap < -30:
                explanations.append("Quick confidence booster ⚡")

        if preference_alignment > 0.7:
            explanations.append("Matches your interests 💡")

        if not explanations:
            explanations.append("Recommended for you")

        why_text = " • ".join(explanations)
        return match_score, zpd, why_text
