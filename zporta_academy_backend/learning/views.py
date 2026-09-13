"""
Learning API Views.
"""
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from learning.composition.container import build_get_study_dashboard_use_case
from learning.models import LearningRecord
from learning.serializers import LearningRecordSerializer


class LearningRecordListView(generics.ListAPIView):
    """Raw list of LearningRecords for the current user."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LearningRecordSerializer

    def get_queryset(self):
        return LearningRecord.objects.filter(
            enrollment__user=self.request.user
        ).select_related("enrollment", "subject")


class StudyDashboardView(APIView):
    """
    Returns:
      - 'enrolled': courses the user has started
      - 'suggested_courses': personalized course recommendations (with fallback)
      - 'suggested_quizzes': personalized quiz recommendations (with fallback)
      - 'next_lessons': lessons next in sequence for enrolled courses
      - 'suggested_lessons': suggested lessons (with fallback)
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        limit = int(request.query_params.get("limit", 5))
        use_case = build_get_study_dashboard_use_case()
        dto = use_case.execute(request.user.id, limit=limit, request_context={"request": request})

        return Response({
            "enrolled": dto.enrolled,
            "suggested_courses": dto.suggested_courses,
            "suggested_quizzes": dto.suggested_quizzes,
            "next_lessons": dto.next_lessons,
            "suggested_lessons": dto.suggested_lessons,
        })
