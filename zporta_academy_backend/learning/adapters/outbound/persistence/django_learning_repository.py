"""
Django Learning Repository Persistence Adapter.
"""
from typing import Any, Dict, List, Optional
from django.contrib.contenttypes.models import ContentType
from analytics.models import ActivityEvent
from courses.models import Course
from courses.serializers import CourseSerializer
from enrollment.models import Enrollment
from enrollment.serializers import EnrollmentSerializer
from learning.application.ports.outbound.learning_repository_port import LearningRepositoryPort
from learning.domain.entities import LearningRecordEntity, StudyDashboardEntity, StudyItemEntity
from learning.models import LearningRecord
from learning.serializers import NextLessonFeedItemSerializer, SuggestedLessonFeedItemSerializer
from lessons.models import Lesson
from quizzes.models import Quiz
from quizzes.serializers import QuizSerializer


class DjangoLearningRepository(LearningRepositoryPort):
    """PostgreSQL / SQLite persistence adapter for study dashboard recommendations and learning records."""

    def __init__(self):
        self._study_items: Dict[int, StudyItemEntity] = {}

    def get_user_learning_records(self, user_id: int) -> List[LearningRecordEntity]:
        qs = LearningRecord.objects.filter(enrollment__user_id=user_id).select_related("enrollment", "subject")
        results = []
        for r in qs:
            results.append(LearningRecordEntity(
                id=r.id,
                enrollment_id=r.enrollment_id,
                subject_id=r.subject_id,
                user_id=user_id,
                username=r.enrollment.user.username if r.enrollment and r.enrollment.user else "",
                content_title=str(r.enrollment.content_object) if r.enrollment else "",
                started_at=r.started_at,
            ))
        return results

    def get_dashboard_aggregates(
        self,
        user_id: int,
        limit: int = 5,
        request_context: Optional[Dict[str, Any]] = None,
    ) -> StudyDashboardEntity:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return StudyDashboardEntity(
                enrolled=[], suggested_courses=[], suggested_quizzes=[], next_lessons=[], suggested_lessons=[]
            )

        context = request_context or {}

        # 1) Enrolled courses
        enroll_qs = Enrollment.objects.filter(user=user, enrollment_type="course")
        enrolled_course_ids = list(enroll_qs.values_list("object_id", flat=True))
        enrolled_serialized = EnrollmentSerializer(enroll_qs, many=True, context=context).data

        # Content Types
        lesson_ct = ContentType.objects.get_for_model(Lesson)
        quiz_ct = ContentType.objects.get_for_model(Quiz)

        # Subject interests
        subject_ids = set()
        events = ActivityEvent.objects.filter(
            user=user,
            event_type__in=["lesson_clicked", "quiz_started", "quiz_submitted", "quiz_answer_submitted"],
        ).select_related("content_type")

        for ev in events:
            try:
                if ev.content_type_id == lesson_ct.id:
                    lesson = Lesson.objects.select_related("course__subject").only("course__subject_id").get(pk=ev.object_id)
                    if lesson.course and lesson.course.subject_id:
                        subject_ids.add(lesson.course.subject_id)
                elif ev.content_type_id == quiz_ct.id:
                    quiz = Quiz.objects.only("subject_id").get(pk=ev.object_id)
                    if quiz.subject_id:
                        subject_ids.add(quiz.subject_id)
            except (Lesson.DoesNotExist, Quiz.DoesNotExist):
                pass

        # 2) Course Suggestions
        course_qs = Course.objects.filter(is_draft=False)
        personalized_course_qs = course_qs
        if subject_ids:
            personalized_course_qs = personalized_course_qs.filter(subject_id__in=subject_ids)
        if enrolled_course_ids:
            personalized_course_qs = personalized_course_qs.exclude(id__in=enrolled_course_ids)

        if personalized_course_qs.exists():
            final_course_qs = personalized_course_qs.order_by("?")[:limit]
        else:
            fallback = course_qs.exclude(id__in=enrolled_course_ids).order_by("-created_at")[:limit]
            final_course_qs = fallback if fallback.exists() else course_qs.order_by("-created_at")[:limit]

        suggested_courses = CourseSerializer(final_course_qs, many=True, context=context).data

        # 3) Quiz Suggestions
        taken_quiz_ids = list(
            ActivityEvent.objects.filter(
                user=user,
                content_type=quiz_ct,
                event_type__in=["quiz_started", "quiz_submitted", "quiz_answer_submitted"],
            )
            .order_by("-timestamp")
            .values_list("object_id", flat=True)
            .distinct()[:20]
        )

        base_quiz_qs = Quiz.objects.all()
        if taken_quiz_ids:
            related_subj_ids = list(
                Quiz.objects.filter(id__in=taken_quiz_ids, subject__isnull=False)
                .values_list("subject_id", flat=True)
                .distinct()
            )
            personalized_quiz_qs = base_quiz_qs.exclude(id__in=taken_quiz_ids)
            if related_subj_ids:
                personalized_quiz_qs = personalized_quiz_qs.filter(subject_id__in=related_subj_ids)

            if personalized_quiz_qs.exists():
                final_quiz_qs = personalized_quiz_qs.order_by("?")[:limit]
            else:
                final_quiz_qs = base_quiz_qs.filter(quiz_type="free").exclude(id__in=taken_quiz_ids).order_by("?")[:limit]
        else:
            final_quiz_qs = base_quiz_qs.filter(quiz_type="free").order_by("-created_at")[:limit]

        if not final_quiz_qs.exists():
            final_quiz_qs = Quiz.objects.all().order_by("-created_at")[:limit]

        suggested_quizzes = QuizSerializer(final_quiz_qs, many=True, context=context).data

        # 4) Lessons Feed
        lessons_qs = Lesson.objects.filter(course_id__in=enrolled_course_ids)
        completed_lesson_ids = list(
            ActivityEvent.objects.filter(
                user=user,
                content_type=lesson_ct,
                event_type__in=["lesson_clicked", "lesson_completed"],
            ).values_list("object_id", flat=True).distinct()
        )

        next_lessons_qs = lessons_qs.exclude(id__in=completed_lesson_ids).order_by("course__title", "id")[:limit]
        next_lessons = NextLessonFeedItemSerializer(next_lessons_qs, many=True, context=context).data

        suggested_lessons_enrolled_qs = lessons_qs.order_by("?")[:limit]
        if suggested_lessons_enrolled_qs.exists():
            final_suggested_lessons_qs = suggested_lessons_enrolled_qs
        else:
            final_suggested_lessons_qs = Lesson.objects.filter(course__is_draft=False).order_by("-created_at")[:limit]

        suggested_lessons = SuggestedLessonFeedItemSerializer(final_suggested_lessons_qs, many=True, context=context).data

        return StudyDashboardEntity(
            enrolled=enrolled_serialized,
            suggested_courses=suggested_courses,
            suggested_quizzes=suggested_quizzes,
            next_lessons=next_lessons,
            suggested_lessons=suggested_lessons,
        )

    def get_study_item(self, item_id: int) -> Optional[StudyItemEntity]:
        return self._study_items.get(item_id)

    def save_study_item(self, item: StudyItemEntity) -> StudyItemEntity:
        self._study_items[item.id or 1] = item
        return item
