from abc import ABC, abstractmethod
from typing import List, Dict, Any


class EmailSenderPort(ABC):
    """Abstract port for sending multipart emails."""

    @abstractmethod
    def send_multipart_email(
        self,
        to_email: str,
        subject: str,
        plain_text: str,
        html_content: str,
        from_name: str = "Zporta Academy",
        fail_silently: bool = False
    ) -> bool:
        """Send an individual multipart email."""
        pass
