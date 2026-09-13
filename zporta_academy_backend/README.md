# Zporta Academy - Backend API (Django REST Framework)

This directory contains the Django REST Framework backend for Zporta Academy, managing user accounts, courses, lessons, quizzes with ELO scoring, AI podcast generation (DailyCast), teacher tools, and mail magazines.

---

## 1. Quick Start: Running on Localhost

### Step 1: Create & Activate Virtual Environment
```bash
python3 -m venv env
source env/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Run Database Migrations
Generate and apply migrations to initialize your local database:
```bash
python manage.py makemigrations --settings=zporta.settings.local
python manage.py migrate --settings=zporta.settings.local
```

### Step 4: Create Superuser (Admin Account)
```bash
python manage.py createsuperuser --settings=zporta.settings.local
```

### Step 5: Start Development Server
```bash
python manage.py runserver 8000 --settings=zporta.settings.local
```

The backend server is accessible at:
- **API Base**: `http://127.0.0.1:8000/api/`
- **Django Admin**: `http://127.0.0.1:8000/administration-zporta-repersentiivie/`
- **Media Files**: `http://127.0.0.1:8000/media/` and `http://127.0.0.1:8000/api/media/`

---

## 2. Settings & Database Configuration

Django settings are modularized under `zporta/settings/`:
- `base.py`: Shared core settings (installed apps, middleware, password validators, REST framework config, logging).
- `local.py`: Local development overrides (defaults to SQLite, `DEBUG = True`, permissive `ALLOWED_HOSTS`, console email backend).
- `production.py`: Production configuration for Ubuntu AWS (MySQL Unix socket, Redis caching, Let's Encrypt HTTPS headers, S3/CDN assets).

### Choosing Local Database (SQLite vs MySQL)
In `zporta/settings/local.py`:

**Option A: SQLite (Recommended for fastest local dev & testing)**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Option B: MySQL (If you have local MySQL / MariaDB installed)**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'zporta_academy',
        'USER': 'root',
        'PASSWORD': 'yourpassword',
        'HOST': '127.0.0.1',
        'PORT': '3306', # or 3307
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES', NAMES utf8mb4",
        },
    }
}
```

---

## 3. External Services & Architecture Trade-offs

The backend is architected with graceful local fallbacks for every external cloud dependency. You **do not** need external services running on localhost.

| Service | In Production | Localhost Development Fallback | Trade-offs & Local Impact |
| :--- | :--- | :--- | :--- |
| **Redis** | Dedicated Redis cache (`django-redis`) & Channel Layer for WebSockets. | `channels.layers.InMemoryChannelLayer` and Django `LocMemCache`. | **Pros:** Zero setup; no background daemon needed.<br>**Cons:** Cache is lost on server restart; WebSockets only sync within the single process. |
| **Celery** | Distributed asynchronous task queue for audio generation & bulk emails. | Synchronous direct execution. | **Pros:** No worker processes or message broker needed.<br>**Cons:** Heavy background tasks (like bulk TTS) run in-process if triggered. |
| **AWS S3** | Cloud object storage bucket for user uploads, PDFs, and MP3 audio. | `USE_AWS = False`. Files save to local `zporta_academy_backend/media/`. | **Pros:** Local instant file saving and reading.<br>**Cons:** Local disk storage only; relative URL paths served via Django `DEBUG` mode. |
| **Firebase Admin** | Sends push notifications to mobile/web clients. | Code catches missing credentials and logs `[WARN] Firebase features disabled (optional).` | **Pros:** App boots cleanly without credentials.<br>**Cons:** Browser push notification triggers are silently skipped. |
| **Email (SMTP)** | Google Workspace SMTP / transactional email service. | Automatic fallback to `django.core.mail.backends.console.EmailBackend`. | **Pros:** No SMTP errors or credentials required.<br>**Cons:** Emails (password resets, invites) print directly into your terminal console instead of sending to actual inboxes. |
| **AI APIs (OpenAI, Gemini, ElevenLabs, Google TTS)** | LLM synthesis for DailyCast podcasts, match scoring, and neural speech audio. | Missing API keys default to `None`. | **Pros:** All standard courses, quizzes, dashboards, and UI work 100% without keys.<br>**Cons:** Clicking "Generate New DailyCast" or "Synthesize Audio" will return an API configuration error until keys are added to `.env`. |

---

## 4. Common Issues & Troubleshooting

### 1. `sqlite3.OperationalError: no such column: users_profile.locale` (or other missing column)
- **Cause:** New fields were added to Django models in code without generating matching migration files.
- **Fix:** Run:
  ```bash
  python manage.py makemigrations --settings=zporta.settings.local
  python manage.py migrate --settings=zporta.settings.local
  ```

### 2. `ERROR: Failed to build 'mysqlclient' when getting requirements to build wheel`
- **Cause:** `mysqlclient` is a C library requiring OS-level MySQL header files (`libmysqlclient-dev`).
- **Fix:** The codebase uses `pymysql` (`pymysql.install_as_MySQLdb()`) which is 100% pure Python and requires no compilation. Ensure `mysqlclient` is commented out in `requirements.txt`.

### 3. Custom Django Admin URL
- **Note:** The default `/admin/` path is intentionally relocated for security.
- **Access Path:** Open `http://127.0.0.1:8000/administration-zporta-repersentiivie/`.

### 4. Static Files Warning: `(?: (staticfiles.W004) The directory '.../static' does not exist.)`
- **Fix:** Create the missing directory:
  ```bash
  mkdir -p static
  ```

### 5. `RequestsDependencyWarning: urllib3 or chardet doesn't match a supported version`
- **Note:** Harmless version mismatch warning emitted by `requests` library; it does not impact runtime execution.

---

## 5. Offline Intelligence Batch Jobs

Zporta Academy includes background intelligence algorithms for ELO difficulty and feed ranking:

```bash
# Compute quiz difficulty scores
python manage.py compute_content_difficulty --days 90 --settings=zporta.settings.local

# Compute learner abilities
python manage.py compute_user_abilities --days 90 --settings=zporta.settings.local

# Compute personalized match scores
python manage.py compute_match_scores --top-n 100 --settings=zporta.settings.local
```

---

## 6. Running Tests

```bash
python manage.py test quizzes.tests --settings=zporta.settings.local
python manage.py test intelligence.tests --settings=zporta.settings.local
python manage.py test dailycast.tests --settings=zporta.settings.local
```
