"""
Use Case: Get Question detail with navigation and quiz context.
"""
from typing import Optional
from core.shared_kernel.domain.result import Result, ok, err
from quizzes.domain.exceptions import QuestionNotFoundError, QuizNotFoundError
from quizzes.application.dtos import (
    QuestionDetailDTO,
    QuestionDTO,
    QuestionNavigationDTO
)
from quizzes.application.ports.outbound.question_repository_port import QuestionRepositoryPort
from quizzes.application.ports.outbound.quiz_repository_port import QuizRepositoryPort


class GetQuestionDetailUseCase:
    def __init__(
        self,
        question_repo: QuestionRepositoryPort,
        quiz_repo: QuizRepositoryPort
    ):
        self._question_repo = question_repo
        self._quiz_repo = quiz_repo

    def execute(self, permalink: str) -> Result[QuestionDetailDTO, Exception]:
        question = self._question_repo.get_by_permalink(permalink)
        if not question:
            return err(QuestionNotFoundError(permalink))

        quiz = self._quiz_repo.get_by_id(question.quiz_id)
        if not quiz:
            return err(QuizNotFoundError(str(question.quiz_id)))

        prev_q, next_q, pos, total = self._question_repo.get_navigation_for_question(
            question.id, question.quiz_id
        )

        nav = QuestionNavigationDTO(
            prev_permalink=prev_q.permalink if prev_q else None,
            prev_number=(pos - 1) if prev_q else None,
            next_permalink=next_q.permalink if next_q else None,
            next_number=(pos + 1) if next_q else None
        )

        q_dto = QuestionDTO(
            id=question.id,
            quiz_id=question.quiz_id,
            question_type=str(question.question_type),
            permalink=question.permalink,
            question_text=question.question_text,
            question_image=question.question_image,
            question_image_alt=question.question_image_alt,
            question_audio=question.question_audio,
            option1=question.option1,
            option2=question.option2,
            option3=question.option3,
            option4=question.option4,
            correct_option=question.correct_option,
            correct_options=question.correct_options,
            correct_answer=question.correct_answer,
            question_data=question.question_data,
            hint1=question.hint1,
            hint2=question.hint2,
            computed_difficulty_score=question.computed_difficulty_score
        )

        detail = QuestionDetailDTO(
            question=q_dto,
            quiz_id=quiz.id,
            quiz_title=quiz.title,
            quiz_permalink=quiz.permalink,
            total_questions=total,
            current_position=pos,
            navigation=nav
        )
        return ok(detail)
