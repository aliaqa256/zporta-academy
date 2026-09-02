---
name: teacher-mail-system
description: Guide for Teacher Content Configuration Dashboard, Mail Magazine editor, and gated lesson preview rules.
---

# Teacher Content Configuration & Mail Magazine System

## 1. Teacher Content Configuration Dashboard
Allows teachers to configure course defaults, display preferences, and student interaction settings.

### Endpoints
- `GET /api/teachers/config/`: Retrieve active teacher configuration.
- `PATCH /api/teachers/config/`: Update configuration properties (e.g. `allow_comments`, `default_reply_window_months`, `preferred_llm_model`).

## 2. Mail Magazine System & Content Gating
Teachers can publish newsletters and course mail magazines. Unauthenticated or non-enrolled students view a gated preview.

### Gated Content Display Logic
- **Authenticated & Enrolled**: Full content rendered.
- **Anonymous / Non-enrolled**:
  - Top 30% of content is displayed normally.
  - Remaining 70% is blurred via CSS (`filter: blur(5px); user-select: none; pointer-events: none;`).
  - Overlay CTA displayed encouraging login / course enrollment.

### Frontend Mail Magazine Editor
- Integrated rich-text / markdown editor with draft auto-saving.
- Supports inline media embed and email template preview.
