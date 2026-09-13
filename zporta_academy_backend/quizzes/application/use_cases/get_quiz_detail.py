"""
Use Case: Get Quiz Detail with questions and access check.
"""
from typing import Optional
from core.shared_kernel.domain.result import Result, ok, err
from quizzes.domain.policies import QuizAccessPolicy
from quizzes.domain.exceptions import QuizNotFoundError, QuizAccessDeniedError
from quizzes.application.dtos import QuizDetailDTO, QuestionDTO
from quizzes.application.ports.outbound.quiz_repository_port import QuizRepositoryPort
from quizzes.application.ports.outbound.question_repository_port import QuestionRepositoryPort


class GetQuizDetailUseCase:
    def __init__(
        self,
        quiz_repo: QuizRepositoryPort,
        question_repo: QuestionRepositoryPort
    ):
        self._quiz_repo = quiz_repo
        self._question_repo = question_repo

    def execute(
        self,
        permalink: str,
        user_id: Optional[int] = None,
        is_staff: bool = False
    ) -> Result[QuizDetailDTO, Exception]:
        quiz = self._quiz_repo.get_by_permalink(permalink)
        if not quiz:
            return err(QuizNotFoundError(permalink))

        if not QuizAccessPolicy.can_view(quiz, user_id=user_id, is_staff=is_staff):
            return err(QuizAccessDeniedError(f"Quiz '{permalink}' is draft and not accessible."))

        questions = self._question_repo.list_by_quiz_id(quiz.id)
        question_dtos = [
            QuestionDTO(
                id=q.id,
                quiz_id=q.quiz_id,
                question_type=str(q.question_type),
                permalink=q.permalink,
                question_text=q.question_text,
                question_image=q.question_image,
                question_image_alt=q.question_image_alt,
                question_audio=q.question_audio,
                option1=q.option1,
                option2=q.option2,
                option3=q.option3,
                option4=q.option4,
                correct_option=q.correct_option,
                correct_options=q.correct_options,
                correct_answer=q.correct_answer,
                question_data=q.question_data,
                hint1=q.hint1,
                hint2=q.hint2,
                computed_difficulty_score=q.computed_difficulty_score
            )
            for q in questions
        ]

        dto = QuizDetailDTO(
            id=quiz.id,
            title=quiz.title,
            content=quiz.content,
            permalink=quiz.permalink,
            quiz_type=str(quiz.quiz_type),
            status=str(quiz.status),
            created_by_id=quiz.created_by_id,
            created_by_name="",
            subject_id=quiz.subject_id,
            subject_name=None,
            course_id=quiz.course_id,
            course_title=None,
            is_locked=quiz.is_locked,
            difficulty_level=str(quiz.difficulty_level) if quiz.difficulty_level else None,
            computed_difficulty_score=quiz.computed_difficulty_score,
            questions=question_dtos
        )
        return ok(dto)
