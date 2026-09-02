---
name: media-and-exports
description: Guide for setting up WeasyPrint for lesson PDF/Word exports, Google Cloud TTS voice integration, and local file storage fallbacks.
---

# Media, Export & Storage Architecture

## 1. Lesson PDF & Word Exports (WeasyPrint)
Lessons can be exported as printable PDFs using WeasyPrint and Word `.docx` documents using python-docx.

### System Dependencies (Linux / Ubuntu / Debian)
WeasyPrint requires native system rendering libraries:
```bash
sudo apt-get update
sudo apt-get install -y \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    fonts-noto-cjk
```

### Testing PDF Generation
```bash
python manage.py test lessons.tests.test_pdf_export
```

### Export Endpoints
- `GET /api/lessons/<id>/export-pdf/`: Returns generated PDF attachment.
- `GET /api/lessons/<id>/export-docx/`: Returns generated Word docx attachment.

## 2. Google Cloud Text-to-Speech (TTS)
- Requires `GOOGLE_APPLICATION_CREDENTIALS` JSON file or valid environment variable.
- Voice profiles:
  - Japanese: `ja-JP-Neural2-B` (Male), `ja-JP-Neural2-C` (Female).
  - English: `en-US-Neural2-F` (Female), `en-US-Neural2-J` (Male).

## 3. Local Media Storage Fallback
When cloud object storage (S3) is not enabled, files are served locally:
- Root: `settings.MEDIA_ROOT`
- URL: `settings.MEDIA_URL` (`/media/`)
- Ensure directories exist before file writing:
  - `MEDIA_ROOT / 'podcasts' / 'episodes'`
  - `MEDIA_ROOT / 'lesson_exports' / 'pdf'`
