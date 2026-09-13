"""
Django implementation of AuthServicePort using Django Auth and DRF Token.
"""
from typing import Optional
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from users.application.ports.outbound.auth_service_port import AuthServicePort


class DjangoAuthService(AuthServicePort):
    def hash_password(self, raw_password: str) -> str:
        return make_password(raw_password)

    def verify_password(self, raw_password: str, hashed_password: str) -> bool:
        return check_password(raw_password, hashed_password)

    def authenticate_credential(self, username_or_email: str, raw_password: str) -> Optional[int]:
        from django.db.models import Q
        user = User.objects.filter(
            Q(username__iexact=username_or_email) | Q(email__iexact=username_or_email)
        ).first()
        if not user:
            return None

        authenticated_user = authenticate(username=user.username, password=raw_password)
        return authenticated_user.id if authenticated_user else None

    def get_or_create_token(self, user_id: int) -> str:
        user = User.objects.get(id=user_id)
        token, _ = Token.objects.get_or_create(user=user)
        return token.key
