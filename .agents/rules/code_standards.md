# Coding Standards & Guidelines for Zporta Academy

## 1. General Principles
- **Maintain backward compatibility**: Schema additions must be nullable or provide robust defaults.
- **Offline ML / Heavy Processing**: Never run long LLM calls or complex scoring synchronously inside hot HTTP request loops without caching or background task delegation.
- **Defensive Error Handling**: Always provide fallback data if AI services or external APIs fail.

## 2. Backend (Django / DRF)
- Follow Django REST Framework best practices for serializers and viewsets.
- Use `select_related` and `prefetch_related` on foreign keys and many-to-many queries to eliminate N+1 problems.
- Denormalize computed metrics (like `computed_difficulty_score`) where frequent list/filter operations are needed.
- Place reusable business logic in service or utility modules (`utils.py`, `services.py`), keeping views and serializers concise.
- Preserve custom admin URLs (`/administration-zporta-repersentiivie/`).

## 3. Frontend (Next.js & React)
- **Styling**: Use Vanilla CSS / CSS Modules with standard CSS custom property tokens for themes (`var(--bg-primary)`, `var(--text-primary)`, `var(--accent-color)`).
- **Dark Mode**: Support light/dark mode transitions smoothly via CSS variables synced with `localStorage` and `data-theme` attribute on the root element.
- **Body Scroll Lock**: Use standard scroll lock hooks/utilities for modals and slide-overs to prevent background document scrolling.
- **SEO**: Ensure meta descriptions, open graph tags, and single `<h1>` hierarchy on all public pages.

## 4. File & Media Handling
- Check `settings.MEDIA_ROOT` and verify directory existence before writing audio or PDF files locally.
- Use relative path generation with Django's default storage backend or `FileSystemStorage`.
