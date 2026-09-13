# feed/services.py

from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from datetime import timedelta
import logging

from quizzes.models import Quiz
from analytics.models import MemoryStat, FeedExposure, QuizAttempt
from quizzes.serializers import QuizSerializer
from users.models import UserPreference

# AI Intelligence imports
try:
    from intelligence.feed_enhancement import (
        get_ai_personalized_quizzes,
        get_ai_challenge_quizzes,
        get_ai_confidence_builders
    )
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    get_ai_personalized_quizzes = None

logger = logging.getLogger(__name__)

def log_quiz_feed_exposure(user, quiz, source):
    """Record that we showed this quiz to the user in this feed."""
    FeedExposure.objects.create(user=user, quiz=quiz, source=source)


def _get_user_prefs(user):
    """Fetch or None."""
    return UserPreference.objects.filter(user=user).first()


def _base_pool(user):
    """
    Core pool: only quizzes whose subject ∈ user.interested_subjects.
    """
    prefs = _get_user_prefs(user)
    qs = Quiz.objects.filter(status='published')
    if not prefs:
        return qs.none()
    if prefs.interested_subjects.exists():
        qs = qs.filter(subject__in=prefs.interested_subjects.all())

    return qs


def _filter_by_language(qs, lang):
    """Cross-database safe JSONField language filter (PostgreSQL + SQLite compatible)."""
    if not lang:
        return qs
    from django.db import connection
    if connection.vendor == 'postgresql':
        return qs.filter(languages__contains=[lang])
    return qs.filter(languages__icontains=str(lang))


def _language_bucket_selection(pool_qs, limit, prefs):
    """
    From pool_qs, pick:
      - 80% quizzes in prefs.languages_spoken[0]
      - 15% quizzes in English
      -  5% other languages
    Ordered by -created_at (newest first) within each bucket.
    """
    if limit <= 0:
        return []

    primary_lang = prefs.languages_spoken[0] if prefs.languages_spoken else "en"
    # Buckets
    primary_qs = _filter_by_language(pool_qs, primary_lang)
    english_qs = _filter_by_language(pool_qs, "en").exclude(id__in=primary_qs)
    other_qs   = pool_qs.exclude(id__in=primary_qs).exclude(id__in=english_qs)

    # Counts
    cnt_primary = int(limit * 0.80)
    cnt_english = int(limit * 0.15)
    cnt_other   = limit - cnt_primary - cnt_english

    selected = list(primary_qs.order_by('-created_at')[:cnt_primary])
    selected += list(english_qs.order_by('-created_at')[:cnt_english])
    selected += list(other_qs.order_by('-created_at')[:cnt_other])

    return selected


def _location_reorder(quizzes, prefs):
    """
    Within `quizzes` (a list), reorder so that:
      - first ~60% are those whose detected_location matches prefs.location
      - then the other ~40%
    If fewer than that, fill from the remainder.
    """
    if not prefs or not prefs.location or not quizzes:
        return quizzes

    lower_loc = prefs.location.lower()
    in_loc    = [q for q in quizzes if (q.detected_location or '').lower() == lower_loc]
    out_loc   = [q for q in quizzes if (q.detected_location or '').lower() != lower_loc]

    target_in = int(len(quizzes) * 0.60)
    final_list = in_loc[:target_in]
    # fill from out_loc
    needed = len(quizzes) - len(final_list)
    final_list += out_loc[:needed]
    # if still short, append remaining in_loc
    if len(final_list) < len(quizzes):
        final_list += in_loc[target_in:]

    return final_list


def get_explore_quizzes(user, limit=10):
    """
    Explore:
      - Subject: must be in user's interested_subjects (via _base_pool)
      - Location: prioritized via _location_reorder
      - Language: preference-aware fallback
      - Exclude: None (all published quizzes in subject pool eligible)
    """
    prefs = _get_user_prefs(user)
    pool  = _base_pool(user)
    if not prefs:
        return []

    # 1) Filter by language too
    filtered = Quiz.objects.filter(
        id__in=[q.id for q in pool]
    )
    primary = (prefs.languages_spoken[0] if prefs.languages_spoken else '') or ''
    primary = primary.lower()
    filtered = _filter_by_language(filtered, primary) if primary else filtered

    # fallback English if no primary-language items available
    if filtered.count() < limit:
        filtered = filtered | _filter_by_language(pool, "en")
    # ultimate fallback: if still empty, take newest subject-only pool
    if filtered.count() == 0:
        filtered = pool

    # 2) Order by newest
    newest = filtered.order_by('-created_at')[:limit]
    # 3) Location reorder
    ordered = _location_reorder(list(newest), prefs)

    # 4) Serialize & expose
    suggestions = []
    for quiz in ordered:
        tried = QuizAttempt.objects.filter(user=user, quiz=quiz).exists()
        why   = "🌎 Latest quizzes to explore" if not tried else "🔄 Quiz available for review"
        log_quiz_feed_exposure(user, quiz, "explore")
        suggestions.append({
            **QuizSerializer(quiz).data,
            "why": why,
            "source": "explore"
        })
    return suggestions


def get_personalized_quizzes(user, limit=50):
    """
    “Personalized” feed: subject → language distribution → location reorder.
    """
    prefs = _get_user_prefs(user)
    pool  = _base_pool(user)
    if not prefs:
        return []

    # 1) Language bucket selection
    if prefs.languages_spoken:
        lang_selected = _language_bucket_selection(pool, limit, prefs)
    else:
        lang_selected = list(pool.order_by('-created_at')[:limit])
    # 2) Location reorder
    final_list = _location_reorder(lang_selected, prefs)

    # 3) Serialize & expose
    suggestions = []
    for quiz in final_list:
        tried = QuizAttempt.objects.filter(user=user, quiz=quiz).exists()
        why   = "🔍 Based on your interests" if not tried else "🔄 Quiz available for review"
        suggestions.append({
            **QuizSerializer(quiz).data,
            "why": why,
            "source": "personalized",
        })
    return suggestions


def get_review_queue(user, limit=50):
    """
    “Review” feed: spaced-repetition items only.
    """
    now     = timezone.now()
    quiz_ct = ContentType.objects.get_for_model(Quiz)

    recent_ids = FeedExposure.objects.filter(
        user=user,
        shown_at__gte=now - timedelta(days=1),
        source="review"
    ).values_list('quiz_id', flat=True)

    stats = MemoryStat.objects.filter(
        user=user,
        content_type=quiz_ct,
        next_review_at__lte=now
    ).exclude(object_id__in=recent_ids).order_by('next_review_at')[:limit]

    suggestions = []
    for stat in stats:
        quiz = stat.learnable_item
        if not quiz:
            continue

        overdue = (now - stat.next_review_at).days
        if stat.repetitions == 0:
            why = "🆕 First-time review"
        elif overdue > 7:
            why = f"🔥 Very overdue! ({overdue} days late)"
        else:
            why = f"🧠 Review now ({overdue} days overdue)"

        log_quiz_feed_exposure(user, quiz, "review")
        suggestions.append({
            **QuizSerializer(quiz).data,
            "why": why,
            "source": "review"
        })
    return suggestions


def generate_user_feed(user, limit=55):
    """
    Unified feed:
      1) Review →
      2) Personalized →
      3) Explore →
      4) Top-up using the same personalized logic (subject→language→location)
    """
    final_feed = []
    seen_ids   = set()
    ten_mins   = timezone.now() - timedelta(minutes=10)

    recently_tried = set(
        QuizAttempt.objects.filter(
            user=user,
            attempted_at__gte=ten_mins
        ).values_list('quiz_id', flat=True)
    )

    def add(items):
        for itm in items:
            if 'status' in itm and itm['status'] != 'published':
                continue
            if itm["id"] not in seen_ids and itm["id"] not in recently_tried:
                final_feed.append(itm)
                seen_ids.add(itm["id"])
                if len(final_feed) >= limit:
                    return True
        return False

    # 1) Review
    if add(get_review_queue(user, limit)):
        return final_feed

    # 2) Personalized (try AI first, fallback to classic)
    if AI_AVAILABLE and get_ai_personalized_quizzes:
        ai_personalized = get_ai_personalized_quizzes(user, limit)
        if ai_personalized and add(ai_personalized):
            return final_feed
    
    # Fallback to classic personalized
    if add(get_personalized_quizzes(user, limit)):
        return final_feed

    # 3) Explore
    if add(get_explore_quizzes(user, limit)):
        return final_feed

    # 4) Top-up: re-run personalized logic for the remaining slots
    remaining = limit - len(final_feed)
    if remaining > 0:
        topup = get_personalized_quizzes(user, remaining)
        add(topup)

    return final_feed
