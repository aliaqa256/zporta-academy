"""
Pure domain policies for Quiz grading and access control.
Zero framework dependencies.
"""
import re
import unicodedata
from typing import Tuple, Any, Optional, List, Dict
from .entities import QuestionEntity, QuizEntity


def normalize_text(s: Any) -> str:
    """Normalize string for robust answer comparison (NFKC, lowercase, collapse whitespace, strip colon)."""
    text = unicodedata.normalize("NFKC", str(s or "")).strip().lower()
    text = re.sub(r"\s+", " ", text)
    if text.endswith(":"):
        text = text[:-1]
    return text


class GradingPolicy:
    """Pure domain logic for checking quiz answers and calculating QoR."""

    @staticmethod
    def evaluate_answer(
        question: QuestionEntity,
        raw_selected_option: Any = None,
        selected_answer_text: Optional[str] = None,
        selected_option_key: Optional[str] = None,
        selected_options: Optional[List[Any]] = None,
    ) -> Tuple[bool, Any, Any]:
        """
        Evaluates a submitted answer against a question entity.
        Returns: (is_correct: bool, correct_value: Any, processed_answer: Any)
        """
        q_type = question.question_type.value if hasattr(question.question_type, "value") else str(question.question_type).lower()
        if "mcq" in q_type:
            q_type = "mcq"
        elif "short" in q_type:
            q_type = "short"
        elif "multi" in q_type:
            q_type = "multi"
        elif "sort" in q_type:
            q_type = "sort"
        elif "drag" in q_type:
            q_type = "dragdrop"

        is_correct = False
        correct_value = None
        processed_answer = raw_selected_option

        if q_type == "mcq":
            try:
                correct_idx = int(question.correct_option or 0)
            except (TypeError, ValueError):
                correct_idx = 0
            correct_value = correct_idx
            
            # Map index (1..4) to option text
            option_texts = {
                1: question.option1,
                2: question.option2,
                3: question.option3,
                4: question.option4,
            }
            correct_text = option_texts.get(correct_idx)

            # 1. Best: exact option TEXT (works regardless of shuffle)
            if selected_answer_text:
                is_correct = normalize_text(selected_answer_text) == normalize_text(correct_text)
                processed_answer = selected_answer_text

            # 2. Exact option key ("option1".."option4")
            elif isinstance(selected_option_key, str) and selected_option_key in {"option1", "option2", "option3", "option4"}:
                opt_map = {
                    "option1": question.option1,
                    "option2": question.option2,
                    "option3": question.option3,
                    "option4": question.option4,
                }
                chosen_text = opt_map.get(selected_option_key)
                is_correct = normalize_text(chosen_text) == normalize_text(correct_text)
                processed_answer = selected_option_key

            # 3. Raw index (1..4)
            else:
                try:
                    raw_int = int(raw_selected_option)
                except (TypeError, ValueError):
                    raw_int = None
                is_correct = (raw_int == correct_idx)
                processed_answer = raw_int

        elif q_type == "short":
            is_correct = normalize_text(raw_selected_option) == normalize_text(question.correct_answer)
            correct_value = question.correct_answer
            processed_answer = raw_selected_option

        elif q_type == "multi":
            selected = selected_options or []
            correct = question.correct_options or []
            is_correct = sorted(map(str, selected)) == sorted(map(str, correct))
            correct_value = correct
            processed_answer = selected

        elif q_type in ("sort", "dragdrop"):
            selected = selected_options or []
            correct = question.correct_options or []
            is_correct = list(map(str, selected)) == list(map(str, correct))
            correct_value = correct
            processed_answer = selected

        return is_correct, correct_value, processed_answer

    @staticmethod
    def calculate_quality_of_recall(is_correct: bool, time_spent_ms: Optional[int]) -> int:
        """Calculates Quality of Recall (1-5) based on correctness and response time."""
        if not is_correct:
            return 1
        if time_spent_ms is None or time_spent_ms > 15000:
            return 3
        if time_spent_ms > 7000:
            return 4
        return 5


class QuizAccessPolicy:
    """Evaluates whether a user can view or interact with a quiz."""

    @staticmethod
    def can_view(quiz: QuizEntity, user_id: Optional[int], is_staff: bool = False) -> bool:
        if quiz.is_published:
            return True
        if user_id is None:
            return False
        return (user_id == quiz.created_by_id) or is_staff

    @staticmethod
    def can_edit(quiz: QuizEntity, user_id: Optional[int], is_staff: bool = False) -> bool:
        if user_id is None:
            return False
        return (user_id == quiz.created_by_id) or is_staff
