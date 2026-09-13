"""
Django ORM implementation of LessonRepositoryPort and LessonCompletionRepositoryPort.
"""
from typing import Optional, List
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from lessons.models import Lesson
from enrollment.models import Enrollment
from analytics.models import ActivityEvent
from lessons.domain.entities import LessonEntity, LessonCompletionEntity
from lessons.application.dtos import LessonFilterQueryDTO, LessonSummaryDTO
from lessons.application.ports.outbound.lesson_repository_port import LessonRepositoryPort
from lessons.application.ports.outbound.lesson_completion_port import LessonCompletionRepositoryPort


class DjangoLessonRepository(LessonRepositoryPort, LessonCompletionRepositoryPort):
    def _map_to_entity(self, lesson: Lesson) -> LessonEntity:
        return LessonEntity(
            id=lesson.id,
            title=lesson.title,
            content=lesson.content,
            permalink=lesson.permalink,
            video_url=lesson.video_url,
            subject_id=lesson.subject_id,
            course_id=lesson.course_id,
            created_by_id=lesson.created_by_id,
            status=lesson.status,
            is_premium=lesson.is_premium,
            is_locked=lesson.is_locked,
            position=getattr(lesson, "position", 0),
            published_at=lesson.published_at,
            created_at=lesson.created_at,
        )

    def get_by_id(self, lesson_id: int) -> Optional[LessonEntity]:
        try:
            lesson = Lesson.objects.get(id=lesson_id)
            return self._map_to_entity(lesson)
        except Lesson.DoesNotExist:
            return None

    def get_by_permalink(self, permalink: str) -> Optional[LessonEntity]:
        try:
            lesson = Lesson.objects.select_related("created_by", "course", "subject").get(permalink=permalink)
            return self._map_to_entity(lesson)
        except Lesson.DoesNotExist:
            return None

    def list_lessons(self, query: LessonFilterQueryDTO) -> List[LessonSummaryDTO]:
        qs = Lesson.objects.all()
        if query.course_id:
            qs = qs.filter(course_id=query.course_id)
        if query.subject_id:
            qs = qs.filter(subject_id=query.subject_id)
        if query.status:
            qs = qs.filter(status=query.status)
        else:
            qs = qs.filter(status=Lesson.PUBLISHED)

        qs = qs.select_related("subject", "course", "created_by")

        results = []
        for l in qs:
            results.append(
                LessonSummaryDTO(
                    id=l.id,
                    title=l.title,
                    permalink=l.permalink,
                    content_preview=l.content[:150] if l.content else "",
                    subject_id=l.subject_id,
                    subject_name=l.subject.name if l.subject else None,
                    course_id=l.course_id,
                    course_title=l.course.title if l.course else None,
                    created_by_id=l.created_by_id,
                    created_by_name=l.created_by.username if l.created_by else "",
                    status=l.status,
                    is_premium=l.is_premium,
                    is_locked=l.is_locked,
                    position=getattr(l, "position", 0),
                    created_at=l.created_at.strftime("%Y-%m-%d") if l.created_at else "",
                )
            )
        return results

    def set_status(self, lesson_id: int, status: str) -> LessonEntity:
        lesson = Lesson.objects.get(id=lesson_id)
        lesson.status = status
        if status == Lesson.PUBLISHED and not lesson.published_at:
            lesson.published_at = timezone.now()
        lesson.save()
        return self._map_to_entity(lesson)

    def is_user_enrolled_in_course(self, user_id: int, course_id: int) -> bool:
        return Enrollment.objects.filter(
            user_id=user_id,
            enrollment_type="course",
            object_id=course_id
        ).exists()

    def is_lesson_completed_by_user(self, user_id: int, lesson_id: int) -> bool:
        lesson_ct = ContentType.objects.get_for_model(Lesson)
        return ActivityEvent.objects.filter(
            user_id=user_id,
            content_type=lesson_ct,
            object_id=lesson_id,
            event_type="lesson_completed"
        ).exists()

    def record_completion(self, user_id: int, lesson_id: int) -> LessonCompletionEntity:
        lesson = Lesson.objects.get(id=lesson_id)
        lesson_ct = ContentType.objects.get_for_model(Lesson)
        
        event, _ = ActivityEvent.objects.get_or_create(
            user_id=user_id,
            content_type=lesson_ct,
            object_id=lesson.id,
            event_type="lesson_completed",
            defaults={
                "metadata": {
                    "lesson_id": lesson.id,
                    "lesson_title": lesson.title,
                    "course_id": lesson.course_id,
                }
            }
        )
        return LessonCompletionEntity(
            id=event.id,
            user_id=user_id,
            lesson_id=lesson_id,
            completed_at=event.timestamp,
        )

    def get_completion(self, user_id: int, lesson_id: int) -> Optional[LessonCompletionEntity]:
        lesson_ct = ContentType.objects.get_for_model(Lesson)
        event = ActivityEvent.objects.filter(
            user_id=user_id,
            content_type=lesson_ct,
            object_id=lesson_id,
            event_type="lesson_completed"
        ).first()
        if not event:
            return None
        return LessonCompletionEntity(
            id=event.id,
            user_id=user_id,
            lesson_id=lesson_id,
            completed_at=event.timestamp,
        )
