"""
Django ORM implementation of QuestionRepositoryPort.
"""
from typing import Optional, List, Tuple
from quizzes.models import Question
from quizzes.domain.entities import QuestionEntity
from quizzes.domain.value_objects import QuestionType
from quizzes.application.ports.outbound.question_repository_port import QuestionRepositoryPort


class DjangoQuestionRepository(QuestionRepositoryPort):
    def get_by_id(self, question_id: int, quiz_id: Optional[int] = None) -> Optional[QuestionEntity]:
        try:
            qs = Question.objects.filter(id=question_id)
            if quiz_id is not None:
                qs = qs.filter(quiz_id=quiz_id)
            m = qs.first()
            return self._to_entity(m) if m else None
        except Question.DoesNotExist:
            return None

    def get_by_permalink(self, permalink: str) -> Optional[QuestionEntity]:
        try:
            m = Question.objects.get(permalink=permalink)
            return self._to_entity(m)
        except Question.DoesNotExist:
            return None

    def list_by_quiz_id(self, quiz_id: int) -> List[QuestionEntity]:
        qs = Question.objects.filter(quiz_id=quiz_id).order_by('id')
        return [self._to_entity(m) for m in qs]

    def get_navigation_for_question(
        self, question_id: int, quiz_id: int
    ) -> Tuple[Optional[QuestionEntity], Optional[QuestionEntity], int, int]:
        all_questions = list(Question.objects.filter(quiz_id=quiz_id).order_by('id'))
        target_idx = None
        for i, q in enumerate(all_questions):
            if q.id == question_id:
                target_idx = i
                break

        if target_idx is None:
            return None, None, 1, len(all_questions)

        prev_m = all_questions[target_idx - 1] if target_idx > 0 else None
        next_m = all_questions[target_idx + 1] if target_idx < len(all_questions) - 1 else None

        prev_entity = self._to_entity(prev_m) if prev_m else None
        next_entity = self._to_entity(next_m) if next_m else None

        return prev_entity, next_entity, target_idx + 1, len(all_questions)

    @staticmethod
    def _to_entity(m: Question) -> QuestionEntity:
        return QuestionEntity(
            id=m.id,
            quiz_id=m.quiz_id,
            question_type=QuestionType(m.question_type) if m.question_type in [e.value for e in QuestionType] else QuestionType.MCQ,
            permalink=m.permalink or "",
            question_text=m.question_text,
            question_image=m.question_image.url if m.question_image else None,
            question_image_alt=m.question_image_alt or "",
            question_audio=m.question_audio.url if m.question_audio else None,
            option1=m.option1,
            option2=m.option2,
            option3=m.option3,
            option4=m.option4,
            correct_option=m.correct_option,
            correct_options=m.correct_options,
            correct_answer=m.correct_answer,
            question_data=m.question_data,
            hint1=m.hint1 or "",
            hint2=m.hint2 or "",
            computed_difficulty_score=m.computed_difficulty_score,
            avg_time_spent_ms=m.avg_time_spent_ms,
            success_rate=m.success_rate
        )
