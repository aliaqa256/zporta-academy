"""
API endpoints for interactive podcasts.

Provides:
- GET /api/podcasts/ - List user's podcasts
- POST /api/podcasts/ - Create new podcast
- GET /api/podcasts/{id}/ - Retrieve podcast details
- PUT /api/podcasts/{id}/ - Update podcast
- GET /api/podcasts/{id}/accuracy-check/ - Verify content accuracy
- GET /api/podcasts/{id}/progress/ - Check student progress
- PUT /api/podcasts/{id}/answers/ - Submit student answers
"""
import logging
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from dailycast.application.dtos.podcast_dtos import GeneratePodcastCommand, SubmitAnswersCommand
from dailycast.composition.container import (
    build_create_podcast_use_case,
    build_evaluate_podcast_accuracy_use_case,
    build_get_student_progress_use_case,
    build_submit_podcast_answers_use_case,
)
from dailycast.domain.exceptions import DailycastError
from dailycast.models import DailyPodcast
from dailycast.serializers import DailyPodcastSerializer

logger = logging.getLogger(__name__)


class DailyPodcastViewSet(viewsets.ModelViewSet):
    """API ViewSet for Daily Podcasts."""

    serializer_class = DailyPodcastSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Only return podcasts for current user or all if staff."""
        user = self.request.user
        if user.is_staff:
            return DailyPodcast.objects.all()
        return DailyPodcast.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        """Create a new podcast via use case."""
        if not request.user.is_staff:
            target_user_id = request.user.id
        else:
            target_user_id = request.data.get("user", request.user.id)
            from django.contrib.auth import get_user_model
            User = get_user_model()
            get_object_or_404(User, id=target_user_id)

        primary_language = request.data.get("primary_language", "en")
        secondary_language = request.data.get("secondary_language", "")
        output_format = request.data.get("output_format", "both")

        try:
            use_case = build_create_podcast_use_case()
            cmd = GeneratePodcastCommand(
                user_id=int(target_user_id),
                primary_language=primary_language,
                secondary_language=secondary_language,
                output_format=output_format,
                requested_by_id=request.user.id,
                request_type="api",
            )
            result = use_case.execute(cmd)
            podcast_model = DailyPodcast.objects.get(pk=result.id)
            serializer = self.get_serializer(podcast_model)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Podcast creation failed: {str(e)}")
            return Response(
                {"error": f"Failed to create podcast: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["get"], url_path="accuracy-check")
    def accuracy_check(self, request, pk=None):
        """Check accuracy of podcast content via domain policy use case."""
        podcast = self.get_object()
        use_case = build_evaluate_podcast_accuracy_use_case()
        result = use_case.execute(podcast.id)

        if result.status == "pending":
            return Response({
                "status": "pending",
                "message": "Podcast still generating. Please check again soon.",
            }, status=status.HTTP_202_ACCEPTED)

        return Response({
            "status": result.status,
            "accuracy_score": result.accuracy_score,
            "issues": result.issues,
            "warnings": result.warnings,
            "metadata": result.metadata,
            "content_checks": result.content_checks,
            "recommendation": result.recommendation,
        })

    @action(detail=True, methods=["get"])
    def progress(self, request, pk=None):
        """Check student progress on this podcast's questions."""
        podcast = self.get_object()
        use_case = build_get_student_progress_use_case()
        try:
            result = use_case.execute({
                "podcast_id": podcast.id,
                "user_id": request.user.id,
                "is_staff": request.user.is_staff,
            })
            return Response({
                "status": result.status,
                "podcast_info": result.podcast_info,
                "progress": result.progress,
                "questions": result.questions,
                "engagement": result.engagement,
                "recommendation": result.recommendation,
            })
        except DailycastError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=["put"])
    def answers(self, request, pk=None):
        """Submit student answers to podcast questions."""
        podcast = self.get_object()
        answers = request.data.get("answers", {})

        use_case = build_submit_podcast_answers_use_case()
        try:
            use_case.execute(SubmitAnswersCommand(
                podcast_id=podcast.id,
                user_id=request.user.id,
                answers=answers,
                is_staff=request.user.is_staff,
            ))
            # Reload and serialize model for complete response compatibility
            podcast.refresh_from_db()
            serializer = self.get_serializer(podcast)
            return Response(serializer.data)
        except DailycastError as e:
            msg = str(e)
            if "Permission denied" in msg:
                return Response({"error": msg}, status=status.HTTP_403_FORBIDDEN)
            return Response({"error": msg}, status=status.HTTP_400_BAD_REQUEST)
