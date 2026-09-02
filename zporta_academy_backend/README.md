# Zporta Academy - Backend API (Django REST Framework)

## Quick Start

### 1. Environment Setup
```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### 2. Database & Migrations
```bash
python manage.py migrate
```

### 3. Running the Server
```bash
python manage.py runserver 8000
```

### 4. Running Offline Intelligence Batch Jobs
```bash
# Compute quiz difficulty scores
python manage.py compute_content_difficulty --days 90

# Compute learner abilities
python manage.py compute_user_abilities --days 90

# Compute personalized match scores
python manage.py compute_match_scores --top-n 100
```

### 5. Running Tests
```bash
python manage.py test quizzes.tests
python manage.py test intelligence.tests
python manage.py test podcasts.tests
```

For full system details and conventions, see [AGENTS.md](file:///../AGENTS.md).
