"""
Use Case: Get all available subjects.
"""
from typing import List
from core.shared_kernel.domain.result import Result, ok, err
from courses.application.dtos import SubjectDTO
from courses.application.ports.outbound.subject_repository_port import SubjectRepositoryPort


class GetSubjectListUseCase:
    def __init__(self, subject_repo: SubjectRepositoryPort):
        self._subject_repo = subject_repo

    def execute(self) -> Result[List[SubjectDTO], Exception]:
        try:
            subjects = self._subject_repo.list_all()
            return ok(subjects)
        except Exception as e:
            return err(e)
