"""
Media & Document Export Domain Policies.
"""
import re
from core.media_export.domain.entities import DocumentExportEntity


class HtmlSanitizationPolicy:
    """Sanitizes raw lesson HTML and injects typography and print stylesheets."""

    @staticmethod
    def clean_html_for_export(html_content: str) -> str:
        if not html_content:
            return ""

        # Remove script tags and contenteditable attributes
        cleaned = re.sub(r"<script.*?>.*?</script>", "", html_content, flags=re.DOTALL | re.IGNORECASE)
        cleaned = re.sub(r'\s*contenteditable="true"', "", cleaned, flags=re.IGNORECASE)
        return cleaned.strip()

    @classmethod
    def build_printable_html(cls, doc: DocumentExportEntity) -> str:
        clean_content = cls.clean_html_for_export(doc.content_html)
        accent = doc.accent_color or "#222E3B"
        custom_css = doc.custom_css or ""

        subject_html = f'<div class="lesson-meta">Subject: {doc.subject_name}</div>' if doc.subject_name else ""
        course_html = f'<div class="lesson-meta">Course: {doc.course_title}</div>' if doc.course_title else ""
        video_html = f'<div class="lesson-video"><strong>Video Resource:</strong> <a href="{doc.video_url}">{doc.video_url}</a></div>' if doc.video_url else ""

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{doc.title}</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm;
            @bottom-right {{
                content: counter(page);
                font-family: 'Noto Sans CJK JP', 'Segoe UI', Tahoma, sans-serif;
                font-size: 0.8rem;
                color: #888;
            }}
        }}
        body {{
            font-family: 'Noto Sans CJK JP', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .lesson-header {{
            text-align: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 3px solid {accent};
        }}
        .lesson-header h1 {{
            color: {accent};
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}
        .lesson-meta {{
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 0.3rem;
        }}
        .lesson-content {{
            margin-top: 2rem;
        }}
        .lesson-content h1, .lesson-content h2, .lesson-content h3 {{
            color: {accent};
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
        }}
        .lesson-video {{
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #ddd;
            font-size: 0.9rem;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }}
        table th, table td {{
            border: 1px solid #ddd;
            padding: 0.75rem;
            text-align: left;
        }}
        table th {{
            background-color: {accent};
            color: white;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background-color: #f4f4f4;
            padding: 1rem;
            border-radius: 5px;
        }}
        {custom_css}
    </style>
</head>
<body>
    <div class="lesson-header">
        <h1>{doc.title}</h1>
        <div class="lesson-meta">Created by: {doc.author_name} | Date: {doc.created_at_str}</div>
        {subject_html}
        {course_html}
    </div>
    <div class="lesson-content">
        {clean_content}
    </div>
    {video_html}
</body>
</html>"""
        return html.strip()


class ExportFilenamePolicy:
    """Formats uniform, download-friendly filenames."""

    @staticmethod
    def generate_filename(lesson_id: int, format_type: str, title: str = "") -> str:
        clean_title = re.sub(r"[^\w\-_.]", "_", title).strip("_")
        if clean_title:
            return f"lesson-{lesson_id}-{clean_title[:30]}.{format_type}"
        return f"lesson-{lesson_id}.{format_type}"
