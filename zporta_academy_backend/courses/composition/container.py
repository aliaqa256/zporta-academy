"""
Composition Root for Courses Domain.
Constructs use cases with concrete adapters.
"""
from courses.adapters.outbound.persistence.django_course_repository import DjangoCourseRepository
from courses.adapters.outbound.persistence.django_subject_repository import DjangoSubjectRepository
from courses.application.use_cases.get_course_catalog import GetCourseCatalogUseCase
from courses.application.use_cases.get_course_detail import GetCourseDetailUseCase
from courses.application.use_cases.publish_course import PublishCourseUseCase, UnpublishCourseUseCase
from courses.application.use_cases.get_subject_list import GetSubjectListUseCase


def build_course_repository() -> DjangoCourseRepository:
    return DjangoCourseRepository()


def build_subject_repository() -> DjangoSubjectRepository:
    return DjangoSubjectRepository()


def build_get_course_catalog_use_case() -> GetCourseCatalogUseCase:
    return GetCourseCatalogUseCase(
        course_repo=build_course_repository()
    )


def build_get_course_detail_use_case() -> GetCourseDetailUseCase:
    return GetCourseDetailUseCase(
        course_repo=build_course_repository()
    )


def build_publish_course_use_case() -> PublishCourseUseCase:
    return PublishCourseUseCase(
        course_repo=build_course_repository()
    )


def build_unpublish_course_use_case() -> UnpublishCourseUseCase:
    return UnpublishCourseUseCase(
        course_repo=build_course_repository()
    )


def build_get_subject_list_use_case() -> GetSubjectListUseCase:
    return GetSubjectListUseCase(
        subject_repo=build_subject_repository()
    )
