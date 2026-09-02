# Zporta Academy - AI Agent Guide & System Reference (AGENTS.md)

This document is the single source of truth for AI coding agents and developers working on **Zporta Academy**.

---

## 1. Project Overview & Architecture

Zporta Academy is a full-stack educational and language-learning platform featuring personalized learning analytics, automated AI podcasts (DailyCast), interactive quizzes with ELO-style difficulty grading, teacher content configuration, and gated mail magazines.

### Technology Stack
- **Backend**: Django 4.x / Django REST Framework (Python 3.10+), Celery (optional async jobs), SQLite (dev) / PostgreSQL (production).
- **Frontend**: Next.js 14 (App/Pages router), React, Vanilla CSS with custom property tokens (supporting light/dark themes), Lucide icons.
- **AI & Speech**:
  - Script & Insight Generation: Google Gemini Flash (`gemini-1.5-flash`), OpenAI GPT-4o Mini (`gpt-4o-mini`), Claude 3.5 Haiku.
  - Text-to-Speech: Google Cloud TTS (`ja-JP-Neural2-B`, `ja-JP-Wavenet-*`, `en-US-Neural2-*`).
- **Document & Media Processing**: WeasyPrint (HTML to PDF), python-docx (Word export), pydub / ffmpeg (Audio stitching).

---

## 2. Directory Structure & App Responsibilities

```
zporta-academy/
├── AGENTS.md                                # This reference guide
├── README.md                                # Developer onboarding guide
├── .agents/                                 # Antigravity customization root
│   ├── rules/
│   │   └── code_standards.md                # Coding conventions & guidelines
│   └── skills/                              # Specialized workflow guides & tools
│       ├── podcast-engine/                  # DailyCast pipeline, prompt templates, TTS
│       ├── intelligence-analytics/          # ELO difficulty, match scores, progress insights
│       ├── media-and-exports/               # WeasyPrint PDF, Word exports, Google TTS
│       └── teacher-mail-system/             # Teacher config dashboard & Mail Magazine gating
├── zporta_academy_backend/                  # Django REST API backend
│   ├── manage.py
│   ├── zporta/                              # Project settings & URL routing
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── local.py
│   │   │   └── production.py
│   │   └── urls.py                          # Main router & administration path
│   ├── users/                               # User authentication, profiles, role system
│   ├── courses/                             # Courses, lessons, enrollment
│   ├── quizzes/                             # Quizzes, questions, attempts, difficulty explanations
│   ├── intelligence/                        # AI analytics, user abilities, match scoring
│   ├── podcasts/                            # DailyCast generation, episodes, audio storage
│   ├── teachers/                            # Teacher content configurations & preferences
│   ├── mail_magazine/                       # Mail magazine issues, subscriptions, gated view
│   └── lessons/                             # Lesson detail, PDF/Word exporters
└── zporta_academy_frontend/
    └── next-frontend/                       # Next.js web application
        ├── src/
        │   ├── components/                  # Reusable UI components
        │   ├── pages/ (or app/)             # Routing pages
        │   ├── styles/                      # Theme tokens, dark theme CSS, globals
        │   └── lib/                         # API clients, auth helpers, utils
        └── package.json
```

---

## 3. Core Systems & Workflows

### 3.1 AI Intelligence & Quiz Difficulty
- **Models**: `UserAbilityProfile` (0-1000 ELO score), `ContentDifficultyProfile` (quiz/question difficulty & success rates), `MatchScore` (Zone of Proximal Development score for feed ranking).
- **Difficulty Display**: 5 levels (🟢 Beginner `<320`, 🟡 Beginner→Medium `320-420`, 🟠 Medium `420-520`, 🔶 Medium→Hard `520-620`, 🔴 Hard/Expert `620+`).
- **Batch Jobs**:
  - `python manage.py compute_content_difficulty --days 90`
  - `python manage.py compute_user_abilities --days 90`
  - `python manage.py compute_match_scores --top-n 100`

### 3.2 DailyCast & Podcast Generation
- **Pipeline**:
  1. Fetch learner ability profile, weak concepts, and spaced-repetition queue.
  2. Synthesize script via LLM with structured timing tags (`[0:00]`, `[PAUSE]`, `[EMPHASIS]`).
  3. Validate script structure (>1500 chars, required sections).
  4. Convert text segments to speech using Google Cloud TTS.
  5. Stitch background intro/outro jingles via `pydub`/`ffmpeg`.
  6. Store MP3 file locally in `MEDIA_ROOT/podcasts/` (fallback when S3 disabled).

### 3.3 Authentication & Permissions
- Custom User Model with explicit role checks:
  - `user.is_teacher` / `user.is_student` / `user.is_staff`.
- Registration serializer validates password strength, username uniqueness, and optional secondary language / target category assignments.
- Custom Django admin path: `/administration-zporta-repersentiivie/`.

### 3.4 Media & Export Engine
- **PDF Generation**: WeasyPrint parses lesson HTML and injects typography styling (requires system packages: `libpango-1.0-0`, `libpangocairo-1.0-0`, `fonts-noto-cjk`).
- **File Storage**: Local filesystem fallback configured under `MEDIA_ROOT` with relative URLs served via `/media/`.

---

## 4. Development & Operation Commands

### Backend Setup & Execution
```bash
cd zporta_academy_backend
source env/bin/activate  # or activate appropriate virtualenv
python manage.py migrate
python manage.py runserver 8000
```

### Frontend Setup & Execution
```bash
cd zporta_academy_frontend/next-frontend
npm install
npm run dev
```

### Running Test Suites
```bash
cd zporta_academy_backend
python manage.py test quizzes.tests
python manage.py test intelligence.tests
python manage.py test podcasts.tests
```

---

## 5. Skills & Specialized Guides

Refer to the `.agents/skills/` directory for detailed execution manuals:
- [Podcast Engine](file:///.agents/skills/podcast-engine/SKILL.md): Prompt schemas, TTS parameters, audio stitching.
- [Intelligence Analytics](file:///.agents/skills/intelligence-analytics/SKILL.md): ELO rating calculations, match scores, offline commands.
- [Media & Exports](file:///.agents/skills/media-and-exports/SKILL.md): WeasyPrint OS dependencies, font configs, local storage fallbacks.
- [Teacher Mail System](file:///.agents/skills/teacher-mail-system/SKILL.md): Content config API, Mail Magazine editor, gating logic.
