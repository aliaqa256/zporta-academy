"""
Django implementation of QuizAnswerLogPort.
"""
from typing import Optional, Dict, Any
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from quizzes.models import Quiz, Question
from quizzes.application.ports.outbound.quiz_answer_log_port import QuizAnswerLogPort
from analytics.utils import update_memory_stat_item, log_event, get_or_create_quiz_session_id

User = get_user_model()


class DjangoQuizAnswerLogAdapter(QuizAnswerLogPort):
    def log_answer_event(
        self,
        user_id: int,
        quiz_id: int,
        question_id: int,
        metadata: Dict[str, Any]
    ) -> None:
        try:
            user = User.objects.get(id=user_id)
            quiz = Quiz.objects.get(id=quiz_id)
            question = Question.objects.get(id=question_id)
        except (User.DoesNotExist, Quiz.DoesNotExist, Question.DoesNotExist):
            return

        session_id = get_or_create_quiz_session_id(user, quiz.id)
        log_event(
            user=user,
            event_type='quiz_answer_submitted',
            instance=question,
            metadata=metadata,
            related_object=quiz,
            session_id=session_id
        )

    def update_question_memory_stat(
        self,
        user_id: int,
        question_id: int,
        quality_of_recall: int,
        time_spent_ms: Optional[int]
    ) -> Optional[str]:
        try:
            user = User.objects.get(id=user_id)
            question = Question.objects.get(id=question_id)
        except (User.DoesNotExist, Question.DoesNotExist):
            return None

        stat = update_memory_stat_item(
            user=user,
            learnable_item=question,
            quality_of_recall=quality_of_recall,
            time_spent_ms=time_spent_ms
        )
        if stat and stat.next_review_at:
            return stat.next_review_at.isoformat()
        return None
