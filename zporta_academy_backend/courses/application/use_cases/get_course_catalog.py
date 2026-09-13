"""
Use Case: Get course catalog with filters.
"""
from typing import List
from core.shared_kernel.domain.result import Result, ok, err
from courses.application.dtos import CourseFilterQueryDTO, CourseSummaryDTO
from courses.application.ports.outbound.course_repository_port import CourseRepositoryPort


class GetCourseCatalogUseCase:
    def __init__(self, course_repo: CourseRepositoryPort):
        self._course_repo = course_repo

    def execute(self, filter_query: CourseFilterQueryDTO) -> Result[List[CourseSummaryDTO], Exception]:
        try:
            courses = self._course_repo.list_courses(filter_query)
            return ok(courses)
        except Exception as e:
            return err(e)
