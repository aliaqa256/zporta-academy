from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.core.mail import EmailMultiAlternatives
from bs4 import BeautifulSoup
from django.conf import settings
from django.utils import timezone
from django.db import models
from django.db.models import Q, Count
from django.contrib.auth import get_user_model
from .models import (
    TeacherMailMagazine, MailMagazineIssue, MailMagazineTemplate, 
    MailMagazineAutomation, RecipientGroup
)
from .serializers import (
    TeacherMailMagazineSerializer, 
    MailMagazineTemplateSerializer,
    MailMagazineAutomationSerializer,
    RecipientGroupSerializer
)
from social.models import GuideRequest
from enrollment.models import Enrollment
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class IsTeacherOrAdmin(BasePermission):
    """Allow access only to guides (teachers) or staff."""

    message = "Only teachers or admins can manage mail magazines."

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if getattr(user, 'is_staff', False) or getattr(user, 'is_superuser', False):
            return True
        profile = getattr(user, 'profile', None)
        role = getattr(profile, 'role', None)
        return role in ('guide', 'both')


class TeacherMailMagazineViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherMailMagazineSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def get_queryset(self):
        return TeacherMailMagazine.objects.filter(teacher=self.request.user)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    @action(detail=True, methods=['post'])
    def send_email(self, request, pk=None):
        """Send email to selected recipients (only followers with mail magazine enabled)"""
        from .composition.container import build_dispatch_mail_magazine_use_case
        from .application.dtos import SendMagazineCommand
        from .domain.exceptions import NoEligibleRecipientsError, MailMagazineAccessDeniedError

        site_url = getattr(settings, 'SITE_URL', 'https://zportaacademy.com')
        site_name = getattr(settings, 'SITE_NAME', 'Zporta Academy')
        site_logo = getattr(settings, 'SITE_LOGO_URL', 'https://zportaacademy.com/logo.png')

        cmd = SendMagazineCommand(
            magazine_id=int(pk),
            teacher_id=request.user.id,
            teacher_username=request.user.username,
            site_url=site_url,
            site_name=site_name,
            site_logo_url=site_logo
        )

        use_case = build_dispatch_mail_magazine_use_case()
        try:
            result = use_case.execute(cmd)
            return Response({
                'success': True,
                'message': result.message,
                'recipients_count': result.recipients_count
            })
        except NoEligibleRecipientsError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except MailMagazineAccessDeniedError as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response(
                {'error': f'Failed to send email: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from .serializers import MailMagazineIssueSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class MailMagazineIssueDetailView(RetrieveAPIView):
    """
    View a sent mail magazine issue.
    Access: teacher who sent it, recipients, or anyone if is_public=True
    """
    queryset = MailMagazineIssue.objects.all()
    serializer_class = MailMagazineIssueSerializer
    permission_classes = [IsAuthenticated]
    
    def retrieve(self, request, *args, **kwargs):
        from .composition.container import build_get_mail_issue_detail_use_case
        from .domain.exceptions import MailMagazineIssueNotFoundError, MailMagazineAccessDeniedError

        use_case = build_get_mail_issue_detail_use_case()
        is_staff = getattr(request.user, 'is_staff', False) or getattr(request.user, 'is_superuser', False)

        try:
            issue_dto = use_case.execute(
                issue_id=self.kwargs.get('pk'),
                requesting_user_id=request.user.id if request.user else None,
                is_staff=is_staff
            )
        except MailMagazineIssueNotFoundError:
            return Response({'error': 'Issue not found.'}, status=status.HTTP_404_NOT_FOUND)
        except MailMagazineAccessDeniedError:
            return Response(
                {'error': 'You do not have permission to view this issue.'},
                status=status.HTTP_403_FORBIDDEN
            )

        issue = self.get_object()
        serializer = self.get_serializer(issue)
        data = serializer.data
        data['html_content'] = issue_dto.html_content
        data['is_gated'] = issue_dto.is_gated
        return Response(data)


class TeacherMailMagazineIssuesListView(ListAPIView):
    """
    List all mail magazine issues by a specific teacher.
    Access: Only shows issues where logged-in user is a recipient or if is_public=True
    """
    serializer_class = MailMagazineIssueSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        username = self.kwargs.get('username')
        teacher = get_object_or_404(User, username=username)
        user = self.request.user
        
        # Get all issues by this teacher
        issues = MailMagazineIssue.objects.filter(magazine__teacher=teacher)
        
        # Filter to only issues the user can access
        # (where user is recipient OR issue is public OR user is the teacher)
        if user == teacher:
            # Teacher sees all their issues
            return issues
        else:
            # Others see only issues they received or public ones
            return issues.filter(
                models.Q(recipients=user) | models.Q(is_public=True)
            ).distinct()


class MailMagazineTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing email templates
    """
    serializer_class = MailMagazineTemplateSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]
    
    def get_queryset(self):
        return MailMagazineTemplate.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def list(self, request, *args, **kwargs):
        """Return user's templates. If none exist, auto-provision default set.

        This avoids empty UI states and gives immediate usable, styled templates.
        """
        qs = self.get_queryset()
        if not qs.exists():
            # Default starter templates (subjects/bodies include variables)
            defaults = [
                {
                    'name': 'Thank You for Attending',
                    'template_type': 'thank_attend',
                    'subject': 'Thank you for attending!',
                    'body': (
                        "<h2 style='color:#ffb703;'>Thank You for Attending!</h2>"
                        "<p>Hello {{student_name}},</p>"
                        "<p>I appreciate you taking time to visit my guide page. Your interest means a lot!"\
                        " Feel free to explore more resources and reach out with any questions.</p>"
                        "<p>Warm regards,<br/>{{teacher_name}}</p>"
                    ),
                },
                {
                    'name': 'Welcome Enrollment',
                    'template_type': 'welcome_enroll',
                    'subject': 'Welcome to {{course_name}}!',
                    'body': (
                        "<h2 style='color:#ffb703;'>Welcome to {{course_name}}!</h2>"
                        "<p>Hello {{student_name}},</p>"
                        "<p>Thrilled to have you onboard. Start with the intro module and set your learning goals."\
                        " I'm here if you need support.</p>"
                        "<p>To your success,<br/>{{teacher_name}}</p>"
                    ),
                },
                {
                    'name': 'Thank You for Purchase',
                    'template_type': 'thank_purchase',
                    'subject': 'Thank you for your purchase!',
                    'body': (
                        "<h2 style='color:#ffb703;'>Thank You for Your Purchase!</h2>"
                        "<p>Hello {{student_name}},</p>"
                        "<p>Thanks for purchasing {{course_name}}. Dive into the first lesson when ready."\
                        " Let me know if you need onboarding help.</p>"
                        "<p>Best,<br/>{{teacher_name}}</p>"
                    ),
                },
                {
                    'name': 'Course Completion Congratulations',
                    'template_type': 'completion',
                    'subject': 'Congratulations on completing {{course_name}}!',
                    'body': (
                        "<h2 style='color:#ffb703;'>🎉 Congratulations!</h2>"
                        "<p>Hi {{student_name}},</p>"
                        "<p>You just completed {{course_name}} — outstanding work! Consider leaving a review and exploring advanced courses.</p>"
                        "<p>Keep growing,<br/>{{teacher_name}}</p>"
                    ),
                },
                {
                    'name': 'Custom Blank Template',
                    'template_type': 'custom',
                    'subject': 'Your custom message',
                    'body': (
                        "<h2 style='color:#ffb703;'>Your Custom Message</h2>"
                        "<p>Hello {{student_name}},</p>"
                        "<p>Write your personalized content here...</p>"
                        "<p>Regards,<br/>{{teacher_name}}</p>"
                    ),
                },
            ]
            created = []
            for item in defaults:
                created.append(MailMagazineTemplate.objects.create(
                    created_by=request.user,
                    **item
                ))
            qs = MailMagazineTemplate.objects.filter(id__in=[t.id for t in created])
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class MailMagazineAutomationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing email automation rules
    """
    serializer_class = MailMagazineAutomationSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]
    
    def get_queryset(self):
        return MailMagazineAutomation.objects.filter(teacher=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class RecipientManagementViewSet(viewsets.ViewSet):
    """
    Advanced recipient management for mail magazines.
    Provides search, filtering, and group management.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def available_students(self, request):
        """
        Get all available attendees (students) for the logged-in teacher.
        Supports search and filtering.
        
        Query parameters:
        - search: Search by username, display_name, or email
        - course_id: Filter by course enrollment
        - status: 'all', 'accepted', 'pending', 'declined'
        """
        teacher = request.user
        search = request.query_params.get('search', '').strip()
        course_id = request.query_params.get('course_id', None)
        guide_status = request.query_params.get('status', 'accepted')

        # Get all attendees (guide requests)
        query = GuideRequest.objects.filter(guide=teacher)
        
        if guide_status != 'all':
            query = query.filter(status=guide_status)
        
        # Get students
        student_ids = query.values_list('explorer_id', flat=True)
        students = User.objects.filter(id__in=student_ids).select_related('profile')

        # Filter by course if specified
        if course_id:
            from courses.models import Course
            course_ct = ContentType.objects.get_for_model(Course)
            enrolled = Enrollment.objects.filter(
                object_id=course_id,
                status='active',
                content_type=course_ct
            ).values_list('user_id', flat=True)
            students = students.filter(id__in=enrolled)

        # Search
        if search:
            students = students.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(profile__display_name__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )

        # Get email preferences
        students_data = []
        for student in students.order_by('username'):
            profile = getattr(student, 'profile', None)
            guide_req = GuideRequest.objects.filter(
                guide=teacher,
                explorer=student
            ).first()
            
            students_data.append({
                'id': student.id,
                'username': student.username,
                'email': student.email,
                'display_name': profile.display_name if profile else student.username,
                'full_name': f"{student.first_name} {student.last_name}".strip() or student.username,
                'guide_status': guide_req.status if guide_req else 'none',
                'email_enabled': profile.mail_magazine_enabled if profile else True,
            })

        return Response({
            'count': len(students_data),
            'students': students_data
        })

    @action(detail=False, methods=['post'])
    def bulk_add_recipients(self, request):
        """Bulk add multiple recipients to a magazine."""
        magazine_id = request.data.get('magazine_id')
        recipient_ids = request.data.get('recipient_ids', [])

        try:
            magazine = TeacherMailMagazine.objects.get(id=magazine_id, teacher=request.user)
            magazine.selected_recipients.add(*recipient_ids)
            return Response({
                'success': True,
                'message': f'Added {len(recipient_ids)} recipients',
                'total_recipients': magazine.selected_recipients.count()
            })
        except TeacherMailMagazine.DoesNotExist:
            return Response(
                {'error': 'Magazine not found or access denied'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'])
    def bulk_remove_recipients(self, request):
        """Bulk remove multiple recipients from a magazine."""
        magazine_id = request.data.get('magazine_id')
        recipient_ids = request.data.get('recipient_ids', [])

        try:
            magazine = TeacherMailMagazine.objects.get(id=magazine_id, teacher=request.user)
            magazine.selected_recipients.remove(*recipient_ids)
            return Response({
                'success': True,
                'message': f'Removed {len(recipient_ids)} recipients',
                'total_recipients': magazine.selected_recipients.count()
            })
        except TeacherMailMagazine.DoesNotExist:
            return Response(
                {'error': 'Magazine not found or access denied'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'])
    def clear_recipients(self, request):
        """Clear all selected recipients from a magazine."""
        magazine_id = request.data.get('magazine_id')

        try:
            magazine = TeacherMailMagazine.objects.get(id=magazine_id, teacher=request.user)
            count = magazine.selected_recipients.count()
            magazine.selected_recipients.clear()
            return Response({
                'success': True,
                'message': f'Cleared {count} recipients',
                'total_recipients': 0
            })
        except TeacherMailMagazine.DoesNotExist:
            return Response(
                {'error': 'Magazine not found or access denied'},
                status=status.HTTP_404_NOT_FOUND
            )


class RecipientGroupViewSet(viewsets.ModelViewSet):
    """
    Manage saved recipient groups for mail campaigns.
    Teachers can create, edit, and reuse recipient groups.
    """
    serializer_class = RecipientGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RecipientGroup.objects.filter(teacher=self.request.user)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

    @action(detail=True, methods=['post'])
    def add_members(self, request, pk=None):
        """Add members to a recipient group."""
        group = self.get_object()
        member_ids = request.data.get('member_ids', [])
        group.members.add(*member_ids)
        return Response({
            'success': True,
            'message': f'Added {len(member_ids)} members',
            'total_members': group.members.count()
        })

    @action(detail=True, methods=['post'])
    def remove_members(self, request, pk=None):
        """Remove members from a recipient group."""
        group = self.get_object()
        member_ids = request.data.get('member_ids', [])
        group.members.remove(*member_ids)
        return Response({
            'success': True,
            'message': f'Removed {len(member_ids)} members',
            'total_members': group.members.count()
        })

    @action(detail=True, methods=['post'])
    def apply_to_magazine(self, request, pk=None):
        """Apply this group to a mail magazine."""
        group = self.get_object()
        magazine_id = request.data.get('magazine_id')

        try:
            magazine = TeacherMailMagazine.objects.get(id=magazine_id, teacher=request.user)
            magazine.selected_recipients.set(group.get_members_queryset())
            return Response({
                'success': True,
                'message': f'Applied group to magazine',
                'recipients_count': magazine.selected_recipients.count()
            })
        except TeacherMailMagazine.DoesNotExist:
            return Response(
                {'error': 'Magazine not found'},
                status=status.HTTP_404_NOT_FOUND
            )

