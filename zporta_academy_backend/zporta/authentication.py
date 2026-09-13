from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication without CSRF enforcement for decoupled frontend APIs.
    This allows API clients (like Next.js) using withCredentials or tokens
    to authenticate without requiring manual CSRF token handshakes for REST endpoints.
    """
    def enforce_csrf(self, request):
        return  # Skip CSRF check for API requests
