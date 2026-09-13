"""
Django ORM implementation of CourseRepositoryPort.
"""
from typing import Optional, List
from django.db.models import Q
from courses.models import Course
from enrollment.models import Enrollment
from courses.domain.entities import CourseEntity
from courses.application.dtos import CourseFilterQueryDTO, CourseSummaryDTO
from courses.application.ports.outbound.course_repository_port import CourseRepositoryPort


class DjangoCourseRepository(CourseRepositoryPort):
    def _map_to_entity(self, course: Course) -> CourseEntity:
        return CourseEntity(
            id=course.id,
            title=course.title,
            description=str(course.description or ""),
            permalink=course.permalink,
            cover_image_url=course.cover_image.url if course.cover_image else None,
            subject_id=course.subject_id,
            created_by_id=course.created_by_id,
            price=float(course.price or 0.0),
            course_type=course.course_type,
            is_draft=course.is_draft,
            is_locked=course.is_locked,
            allowed_tester_ids=list(course.allowed_testers.values_list("id", flat=True)),
            created_at=course.created_at,
        )

    def get_by_id(self, course_id: int) -> Optional[CourseEntity]:
        try:
            course = Course.all_objects.get(id=course_id)
            return self._map_to_entity(course)
        except (Course.DoesNotExist, AttributeError):
            try:
                course = Course.objects.get(id=course_id)
                return self._map_to_entity(course)
            except Course.DoesNotExist:
                return None

    def get_by_permalink(self, permalink: str) -> Optional[CourseEntity]:
        try:
            course = Course.all_objects.prefetch_related("allowed_testers").get(permalink=permalink)
            return self._map_to_entity(course)
        except (Course.DoesNotExist, AttributeError):
            try:
                course = Course.objects.prefetch_related("allowed_testers").get(permalink=permalink)
                return self._map_to_entity(course)
            except Course.DoesNotExist:
                return None

    def list_courses(self, filter_query: CourseFilterQueryDTO) -> List[CourseSummaryDTO]:
        qs = Course.all_objects.all() if filter_query.include_drafts else Course.objects.all()

        if filter_query.subject_id:
            qs = qs.filter(subject_id=filter_query.subject_id)

        if filter_query.search_query:
            qs = qs.filter(
                Q(title__icontains=filter_query.search_query) | Q(description__icontains=filter_query.search_query)
            )

        qs = qs.select_related("subject", "created_by").prefetch_related("lessons")

        results = []
        for c in qs:
            results.append(
                CourseSummaryDTO(
                    id=c.id,
                    title=c.title,
                    description=str(c.description or ""),
                    permalink=c.permalink,
                    price=float(c.price or 0.0),
                    course_type=c.course_type,
                    cover_image_url=c.cover_image.url if c.cover_image else None,
                    subject_id=c.subject_id,
                    subject_name=c.subject.name if c.subject else None,
                    created_by_id=c.created_by_id,
                    created_by_name=c.created_by.username if c.created_by else "",
                    lesson_count=c.lessons.count(),
                    is_draft=c.is_draft,
                    is_locked=c.is_locked,
                )
            )
        return results

    def set_draft_status(self, course_id: int, is_draft: bool) -> CourseEntity:
        course = Course.all_objects.get(id=course_id) if hasattr(Course, "all_objects") else Course.objects.get(id=course_id)
        course.is_draft = is_draft
        course.save(update_fields=["is_draft"])
        return self._map_to_entity(course)

    def has_active_enrollments(self, course_id: int) -> bool:
        return Enrollment.objects.filter(
            enrollment_type="course",
            object_id=course_id
        ).exists()
