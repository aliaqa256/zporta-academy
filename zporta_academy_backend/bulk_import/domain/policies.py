from typing import Dict, Any, List
from .entities import ValidationIssue, ValidationReportEntity


class BulkImportValidationPolicy:
    """Pure domain logic for validating JSON curriculum and quiz import payloads."""

    @classmethod
    def validate_curriculum_payload(cls, data: Any) -> ValidationReportEntity:
        errors: List[ValidationIssue] = []
        warnings: List[ValidationIssue] = []

        if not isinstance(data, (dict, list)):
            errors.append(ValidationIssue(level="error", path="root", message="Payload must be a JSON object or array."))
            return ValidationReportEntity(is_valid=False, errors=errors)

        courses_data = data.get("courses", []) if isinstance(data, dict) else (data if isinstance(data, list) else [])
        standalone_quizzes = data.get("quizzes", []) if isinstance(data, dict) else []

        total_courses = len(courses_data)
        total_lessons = 0
        total_quizzes = len(standalone_quizzes)
        total_questions = 0

        # Validate courses
        for idx, course in enumerate(courses_data):
            c_path = f"courses[{idx}]"
            if not isinstance(course, dict):
                errors.append(ValidationIssue(level="error", path=c_path, message="Course entry must be an object."))
                continue

            if not course.get("title"):
                errors.append(ValidationIssue(level="error", path=f"{c_path}.title", message="Course title is required."))

            lessons = course.get("lessons", [])
            total_lessons += len(lessons)
            for l_idx, lesson in enumerate(lessons):
                l_path = f"{c_path}.lessons[{l_idx}]"
                if not isinstance(lesson, dict):
                    errors.append(ValidationIssue(level="error", path=l_path, message="Lesson entry must be an object."))
                    continue
                if not lesson.get("title"):
                    errors.append(ValidationIssue(level="error", path=f"{l_path}.title", message="Lesson title is required."))

                quizzes = lesson.get("quizzes", [])
                total_quizzes += len(quizzes)
                for q_idx, quiz in enumerate(quizzes):
                    q_path = f"{l_path}.quizzes[{q_idx}]"
                    q_errors, q_questions = cls._validate_quiz(quiz, q_path)
                    errors.extend(q_errors)
                    total_questions += q_questions

        # Validate standalone quizzes
        for q_idx, quiz in enumerate(standalone_quizzes):
            q_path = f"quizzes[{q_idx}]"
            q_errors, q_questions = cls._validate_quiz(quiz, q_path)
            errors.extend(q_errors)
            total_questions += q_questions

        return ValidationReportEntity(
            is_valid=(len(errors) == 0),
            errors=errors,
            warnings=warnings,
            total_courses=total_courses,
            total_lessons=total_lessons,
            total_quizzes=total_quizzes,
            total_questions=total_questions
        )

    @classmethod
    def _validate_quiz(cls, quiz: Any, path: str) -> (List[ValidationIssue], int):
        errors: List[ValidationIssue] = []
        if not isinstance(quiz, dict):
            return [ValidationIssue(level="error", path=path, message="Quiz must be an object.")], 0

        if not quiz.get("title"):
            errors.append(ValidationIssue(level="error", path=f"{path}.title", message="Quiz title is required."))

        questions = quiz.get("questions", [])
        for q_idx, q in enumerate(questions):
            q_path = f"{path}.questions[{q_idx}]"
            if not isinstance(q, dict):
                errors.append(ValidationIssue(level="error", path=q_path, message="Question must be an object."))
                continue
            if not q.get("text") and not q.get("prompt"):
                errors.append(ValidationIssue(level="error", path=f"{q_path}.text", message="Question text or prompt is required."))

        return errors, len(questions)
