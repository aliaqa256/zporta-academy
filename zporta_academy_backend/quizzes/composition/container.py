"""
Composition Root for Quizzes Domain.
Constructs use cases with concrete adapters.
"""
from quizzes.adapters.outbound.persistence.django_quiz_repository import DjangoQuizRepository
from quizzes.adapters.outbound.persistence.django_question_repository import DjangoQuestionRepository
from quizzes.adapters.outbound.logging.django_quiz_answer_log_adapter import DjangoQuizAnswerLogAdapter
from quizzes.application.use_cases.get_quiz_detail import GetQuizDetailUseCase
from quizzes.application.use_cases.evaluate_quiz_answer import EvaluateQuizAnswerUseCase
from quizzes.application.use_cases.get_question_detail import GetQuestionDetailUseCase


def build_quiz_repository() -> DjangoQuizRepository:
    return DjangoQuizRepository()


def build_question_repository() -> DjangoQuestionRepository:
    return DjangoQuestionRepository()


def build_quiz_answer_log_adapter() -> DjangoQuizAnswerLogAdapter:
    return DjangoQuizAnswerLogAdapter()


def build_get_quiz_detail_use_case() -> GetQuizDetailUseCase:
    return GetQuizDetailUseCase(
        quiz_repo=build_quiz_repository(),
        question_repo=build_question_repository()
    )


def build_evaluate_quiz_answer_use_case() -> EvaluateQuizAnswerUseCase:
    return EvaluateQuizAnswerUseCase(
        quiz_repo=build_quiz_repository(),
        question_repo=build_question_repository(),
        log_port=build_quiz_answer_log_adapter()
    )


def build_get_question_detail_use_case() -> GetQuestionDetailUseCase:
    return GetQuestionDetailUseCase(
        question_repo=build_question_repository(),
        quiz_repo=build_quiz_repository()
    )
