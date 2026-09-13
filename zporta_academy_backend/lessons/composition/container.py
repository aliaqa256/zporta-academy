"""
Composition Root for Lessons Domain.
Constructs use cases with concrete adapters.
"""
from lessons.adapters.outbound.persistence.django_lesson_repository import DjangoLessonRepository
from lessons.application.use_cases.get_lesson_detail import GetLessonDetailUseCase
from lessons.application.use_cases.complete_lesson import CompleteLessonUseCase
from lessons.application.use_cases.publish_lesson import PublishLessonUseCase, ListLessonsUseCase


def build_lesson_repository() -> DjangoLessonRepository:
    return DjangoLessonRepository()


def build_get_lesson_detail_use_case() -> GetLessonDetailUseCase:
    return GetLessonDetailUseCase(
        lesson_repo=build_lesson_repository()
    )


def build_complete_lesson_use_case() -> CompleteLessonUseCase:
    repo = build_lesson_repository()
    return CompleteLessonUseCase(
        lesson_repo=repo,
        completion_repo=repo
    )


def build_publish_lesson_use_case() -> PublishLessonUseCase:
    return PublishLessonUseCase(
        lesson_repo=build_lesson_repository()
    )


def build_list_lessons_use_case() -> ListLessonsUseCase:
    return ListLessonsUseCase(
        lesson_repo=build_lesson_repository()
    )
