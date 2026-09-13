from typing import Optional
from core.shared_kernel.domain.result import Result, ok, err
from quizzes.domain.policies import GradingPolicy, QuizAccessPolicy
from quizzes.domain.exceptions import QuizNotFoundError, QuestionNotFoundError, QuizAccessDeniedError
from quizzes.application.dtos import RecordAnswerCommand, AnswerEvaluationResultDTO
from quizzes.application.ports.outbound.quiz_repository_port import QuizRepositoryPort
from quizzes.application.ports.outbound.question_repository_port import QuestionRepositoryPort
from quizzes.application.ports.outbound.quiz_answer_log_port import QuizAnswerLogPort


class EvaluateQuizAnswerUseCase:
    def __init__(
        self,
        quiz_repo: QuizRepositoryPort,
        question_repo: QuestionRepositoryPort,
        log_port: Optional[QuizAnswerLogPort] = None
    ):
        self._quiz_repo = quiz_repo
        self._question_repo = question_repo
        self._log_port = log_port

    def execute(
        self,
        cmd: RecordAnswerCommand,
        is_staff: bool = False
    ) -> Result[AnswerEvaluationResultDTO, Exception]:
        question = self._question_repo.get_by_id(cmd.question_id, quiz_id=cmd.quiz_id)
        if not question:
            return err(QuestionNotFoundError(str(cmd.question_id)))

        quiz = self._quiz_repo.get_by_id(cmd.quiz_id)
        if not quiz:
            return err(QuizNotFoundError(str(cmd.quiz_id)))

        # Check access to unpublished quizzes
        if not QuizAccessPolicy.can_view(quiz, user_id=cmd.user_id, is_staff=is_staff):
            return err(QuizAccessDeniedError("Cannot submit answers to a draft quiz."))

        # Evaluate answer via pure domain policy
        is_correct, correct_val, processed_ans = GradingPolicy.evaluate_answer(
            question=question,
            raw_selected_option=cmd.selected_option,
            selected_answer_text=cmd.selected_answer_text,
            selected_option_key=cmd.selected_option_key,
            selected_options=cmd.selected_options,
        )

        qor = GradingPolicy.calculate_quality_of_recall(
            is_correct=is_correct,
            time_spent_ms=cmd.time_spent_ms
        )

        next_review_at = None
        if self._log_port:
            next_review_at = self._log_port.update_question_memory_stat(
                user_id=cmd.user_id,
                question_id=cmd.question_id,
                quality_of_recall=qor,
                time_spent_ms=cmd.time_spent_ms
            )

        result = AnswerEvaluationResultDTO(
            is_correct=is_correct,
            message="Answer recorded.",
            quality_of_recall=qor,
            next_review_at=next_review_at,
            processed_answer=processed_ans,
            correct_expected=correct_val
        )
        return ok(result)
