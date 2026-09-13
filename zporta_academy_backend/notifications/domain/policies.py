from typing import Optional


class NotificationFormattingPolicy:
    """Pure domain rules for title, body, and deep link formatting."""

    @staticmethod
    def format_title_and_body(
        title: Optional[str],
        message: str,
        default_title: str = "Zporta Academy"
    ) -> (str, str):
        clean_title = (title or "").strip() or default_title
        clean_message = (message or "").strip()
        return clean_title, clean_message

    @staticmethod
    def normalize_link(link: Optional[str], base_domain: str = "https://zportaacademy.com") -> str:
        if not link or not isinstance(link, str) or not link.strip():
            return f"{base_domain.rstrip('/')}/"
        s = link.strip()
        if s.startswith("https://") or s.startswith("http://"):
            return s
        if s.startswith("/"):
            return f"{base_domain.rstrip('/')}{s}"
        return f"{base_domain.rstrip('/')}/{s}"
