from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from mailmagazine.application.ports.outbound.email_sender_port import EmailSenderPort


class DjangoEmailSenderAdapter(EmailSenderPort):
    """Django Core Mail implementation of EmailSenderPort."""

    def send_multipart_email(
        self,
        to_email: str,
        subject: str,
        plain_text: str,
        html_content: str,
        from_name: str = "Zporta Academy",
        fail_silently: bool = False
    ) -> bool:
        try:
            host_user = getattr(settings, 'EMAIL_HOST_USER', 'noreply@zportaacademy.com')
            from_email_with_name = f"{from_name} <{host_user}>"

            msg = EmailMultiAlternatives(
                subject=subject,
                body=plain_text,
                from_email=from_email_with_name,
                to=[to_email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=fail_silently)
            return True
        except Exception:
            if not fail_silently:
                raise
            return False
