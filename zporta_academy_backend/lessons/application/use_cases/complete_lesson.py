"""
Use Case: Complete lesson and record points.
"""
from core.shared_kernel.domain.result import Result, ok, err
from lessons.domain.exceptions import LessonNotFoundError
from lessons.application.dtos import CompleteLessonCommand, LessonCompletionResultDTO
from lessons.application.ports.outbound.lesson_repository_port import LessonRepositoryPort
from lessons.application.ports.outbound.lesson_completion_port import LessonCompletionRepositoryPort


class CompleteLessonUseCase:
    def __init__(
        self,
        lesson_repo: LessonRepositoryPort,
        completion_repo: LessonCompletionRepositoryPort
    ):
        self._lesson_repo = lesson_repo
        self._completion_repo = completion_repo

    def execute(self, cmd: CompleteLessonCommand) -> Result[LessonCompletionResultDTO, Exception]:
        lesson = self._lesson_repo.get_by_id(cmd.lesson_id)
        if not lesson:
            return err(LessonNotFoundError(str(cmd.lesson_id)))

        # Record completion
        self._completion_repo.record_completion(user_id=cmd.user_id, lesson_id=cmd.lesson_id)

        result = LessonCompletionResultDTO(
            lesson_id=cmd.lesson_id,
            user_id=cmd.user_id,
            points_awarded=2,  # +2 points for lesson completion
            message="Lesson marked as complete."
        )
        return ok(result)
