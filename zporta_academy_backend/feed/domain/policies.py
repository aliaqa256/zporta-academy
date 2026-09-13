from typing import List
from .entities import FeedQuizItemEntity


class FeedRankingPolicy:
    """Pure domain logic for sorting, ranking, and deduplicating feed quiz items."""

    @staticmethod
    def rank_personalized_items(
        items: List[FeedQuizItemEntity],
        limit: int = 10
    ) -> List[FeedQuizItemEntity]:
        """Ranks items by highest match score and caps at limit."""
        sorted_items = sorted(items, key=lambda x: x.match_score, reverse=True)
        return sorted_items[:limit]

    @staticmethod
    def filter_excluded(
        items: List[FeedQuizItemEntity],
        exclude_ids: List[int]
    ) -> List[FeedQuizItemEntity]:
        """Filters out already seen or excluded items."""
        if not exclude_ids:
            return items
        exclude_set = set(exclude_ids)
        return [item for item in items if item.id not in exclude_set]
