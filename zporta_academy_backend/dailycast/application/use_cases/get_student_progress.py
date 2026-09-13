"""
Get Student Progress Use Case.
"""
from typing import Any, Dict
from dailycast.application.dtos.podcast_dtos import StudentProgressDTO
from dailycast.application.ports.outbound.dailycast_repository_port import DailyCastRepositoryPort
from dailycast.domain.exceptions import DailycastError, DailyPodcastNotFoundError


class GetStudentProgressUseCase:
    """Use case to compute and return student engagement and QA progress for a podcast."""

    def __init__(self, repository: DailyCastRepositoryPort):
        self.repository = repository

    def execute(self, request: Dict[str, Any]) -> StudentProgressDTO:
        podcast_id = request.get("podcast_id")
        user_id = request.get("user_id")
        is_staff = request.get("is_staff", False)

        podcast = self.repository.get_by_id(podcast_id)
        if not podcast:
            raise DailyPodcastNotFoundError(podcast_id)

        if podcast.user_id != user_id and not is_staff:
            raise DailycastError("Permission denied")

        user_stats = self.repository.get_user_stats(podcast.user_id)
        username = user_stats.get("username", f"User {podcast.user_id}")

        questions = podcast.questions_asked or []
        answers = podcast.student_answers or {}

        answered_count = len([q for q in questions if answers.get(str(q))])
        completion_percentage = int((answered_count / len(questions) * 100)) if questions else 0

        questions_detail = []
        for i, question in enumerate(questions):
            q_key = str(question)
            user_answer = answers.get(q_key, "")
            questions_detail.append({
                "index": i + 1,
                "question": question,
                "user_answer": user_answer if user_answer else None,
                "answered": bool(user_answer),
                "status": "answered" if user_answer else "pending",
            })

        overall_status = "completed" if completion_percentage == 100 else "in_progress" if answered_count > 0 else "not_started"

        recommendation = (
            "✅ All questions answered" if completion_percentage == 100
            else f"📊 {answered_count}/{len(questions)} questions answered"
        )

        return StudentProgressDTO(
            status="success",
            podcast_info={
                "id": podcast.id,
                "user": username,
                "primary_language": podcast.primary_language,
                "created_at": podcast.created_at.isoformat() if podcast.created_at else None,
            },
            progress={
                "questions_count": len(questions),
                "answered_count": answered_count,
                "completion_percentage": completion_percentage,
                "overall_status": overall_status,
            },
            questions=questions_detail,
            engagement={
                "time_spent_minutes": user_stats.get("time_spent_minutes", 0),
                "last_activity": podcast.updated_at.isoformat() if podcast.updated_at else None,
            },
            recommendation=recommendation,
        )
