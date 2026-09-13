import re
from typing import Dict, Any, List, Optional
from .entities import RecipientInfo


class GatedPreviewPolicy:
    """Pure domain rules governing access and preview gating for mail magazine issues."""

    @staticmethod
    def can_view_full_issue(
        user_id: Optional[int],
        is_staff: bool,
        is_teacher: bool,
        recipient_ids: List[int],
        is_public: bool
    ) -> bool:
        """Determines if the requesting user has full access to read the issue."""
        if is_staff or is_teacher or is_public:
            return True
        if user_id is not None and user_id in recipient_ids:
            return True
        return False

    @staticmethod
    def apply_content_gating(
        html_content: str,
        is_authorized: bool,
        preview_chars: int = 300
    ) -> str:
        """
        Truncates content for unauthorized users or returns full content if authorized.
        """
        if is_authorized or not html_content:
            return html_content

        # Simple text length truncation while stripping script tags
        clean_content = re.sub(r'<script.*?>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        if len(clean_content) <= preview_chars:
            return clean_content + "<p><em>[End of preview - Subscribe to view full issues]</em></p>"

        truncated = clean_content[:preview_chars]
        # Close any open tags simply
        return f"{truncated}...<p style='color:#ffb703;font-weight:bold;'>[Preview truncated. Subscribe to receive full issues from this guide.]</p>"


class TemplateRenderingPolicy:
    """Pure rendering policy for placeholder replacement and email HTML framing."""

    @staticmethod
    def render_placeholders(text: str, variables: Dict[str, Any]) -> str:
        if not text:
            return ""
        pattern = re.compile(r'{{\s*([a-zA-Z0-9_]+)\s*}}')
        return pattern.sub(lambda m: str(variables.get(m.group(1), '')), text)

    @staticmethod
    def build_email_html_wrapper(
        site_name: str,
        site_url: str,
        site_logo: str,
        view_in_browser_url: str,
        content_html: str
    ) -> str:
        return f"""
<html>
  <head>
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  </head>
  <body style='background:#0b1523;margin:0;padding:24px;font-family:"Segoe UI",Arial,sans-serif;color:#ffffff;'>
    <div style='max-width:600px;margin:0 auto;background:#142233;padding:0;border-radius:8px;overflow:hidden;'>
      <div style='background:linear-gradient(135deg, #1e293b 0%, #0f1419 100%);padding:20px 32px;text-align:center;border-bottom:2px solid #ffb703;'>
        <a href='{site_url}' style='display:inline-block;text-decoration:none;'>
          <img src='{site_logo}' alt='{site_name}' style='max-height:50px;width:auto;margin-bottom:10px;display:block;'>
        </a>
        <h1 style='margin:0;font-size:18px;color:#ffb703;font-weight:600;'>From {site_name}</h1>
      </div>
      <div style='background:#0b1523;padding:12px 32px;text-align:center;border-bottom:1px solid #1e293b;'>
        <p style='margin:0;font-size:12px;color:#94a3b8;'>Having trouble viewing this email? <a href='{view_in_browser_url}' style='color:#ffb703;text-decoration:none;font-weight:600;'>View in browser</a></p>
      </div>
      <div style='padding:32px;'>
        {content_html}
      </div>
      <div style='background:#0b1523;padding:24px 32px;border-top:1px solid #1f2e40;'>
        <hr style='border:none;border-top:1px solid #1f2e40;margin:0 0 16px 0;' />
        <p style='font-size:12px;color:#94a3b8;margin:0 0 8px 0;'>You are receiving this because you subscribed to this teacher's mail magazine on {site_name}.</p>
        <p style='font-size:12px;color:#94a3b8;margin:0;'>
          <a href='{site_url}/preferences/mail-magazines' style='color:#ffb703;text-decoration:none;font-weight:600;'>Manage preferences</a> | 
          <a href='{site_url}' style='color:#ffb703;text-decoration:none;font-weight:600;'>Visit {site_name}</a>
        </p>
        <p style='font-size:11px;color:#64748b;margin:12px 0 0 0;'>© 2024 {site_name}. All rights reserved.</p>
      </div>
    </div>
  </body>
</html>
""".strip()


class RecipientEligibilityPolicy:
    """Filters recipients based on active opt-in and valid email presence."""

    @staticmethod
    def filter_eligible_recipients(
        candidates: List[RecipientInfo],
        filter_ids: Optional[List[int]] = None
    ) -> List[RecipientInfo]:
        eligible = [
            c for c in candidates
            if c.email and c.mail_magazine_enabled
        ]
        if filter_ids is not None and len(filter_ids) > 0:
            target_set = set(filter_ids)
            eligible = [c for c in eligible if c.id in target_set]
        return eligible
