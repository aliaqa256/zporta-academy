"""
Django ORM implementation of SubjectRepositoryPort.
"""
from typing import Optional, List
from subjects.models import Subject
from courses.domain.entities import SubjectEntity
from courses.application.dtos import SubjectDTO
from courses.application.ports.outbound.subject_repository_port import SubjectRepositoryPort


class DjangoSubjectRepository(SubjectRepositoryPort):
    def get_by_id(self, subject_id: int) -> Optional[SubjectEntity]:
        try:
            s = Subject.objects.get(id=subject_id)
            return SubjectEntity(
                id=s.id,
                name=s.name,
                permalink=s.permalink,
                created_by_id=s.created_by_id,
            )
        except Subject.DoesNotExist:
            return None

    def list_all(self) -> List[SubjectDTO]:
        subjects = Subject.objects.all().order_by("name")
        return [
            SubjectDTO(
                id=s.id,
                name=s.name,
                permalink=s.permalink,
                created_by_id=s.created_by_id,
            )
            for s in subjects
        ]
