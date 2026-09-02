# Zporta Academy

Zporta Academy is a personalized educational platform featuring automated AI podcasts, adaptive quiz difficulty scoring, teacher management tools, and interactive lessons.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- ffmpeg (for podcast audio processing)
- WeasyPrint system libraries (for PDF export: `libpango-1.0-0`, `libpangocairo-1.0-0`)

### Backend Setup
```bash
cd zporta_academy_backend
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup
```bash
cd zporta_academy_frontend/next-frontend
npm install
npm run dev
```

---

## 📚 Documentation & Architecture

- **[AGENTS.md](file:///AGENTS.md)**: Master architecture reference, system diagrams, and coding guidelines.
- **`.agents/skills/`**: Specialized execution guides:
  - [Podcast Engine](file:///.agents/skills/podcast-engine/SKILL.md): DailyCast generation pipeline, prompt schemas, Google TTS.
  - [Intelligence Analytics](file:///.agents/skills/intelligence-analytics/SKILL.md): ELO difficulty scoring & recommendation algorithms.
  - [Media & Exports](file:///.agents/skills/media-and-exports/SKILL.md): WeasyPrint PDF setup and storage configuration.
  - [Teacher Mail System](file:///.agents/skills/teacher-mail-system/SKILL.md): Mail Magazine editor and content gating logic.

---

## 🛠️ Testing
```bash
cd zporta_academy_backend
python manage.py test
```
