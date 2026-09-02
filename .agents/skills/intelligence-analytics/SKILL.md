---
name: intelligence-analytics
description: Guide for ELO-style quiz difficulty scoring, user ability profiling, match score recommendations, and offline management jobs.
---

# Intelligence Analytics & Quiz Difficulty System

## 1. Overview
The `intelligence` Django app provides an ELO-based adaptive difficulty and recommendation engine for quizzes, questions, and students.

## 2. Core Models
- `UserAbilityProfile`: Measures learner skill on a 0-1000 scale, with subject breakdowns, percentile, and global rank.
- `ContentDifficultyProfile`: Dynamic difficulty calculated from user attempt counts, success rates, and average time spent.
- `MatchScore`: Zone of Proximal Development (ZPD) score measuring user-content affinity for ranking personalized feeds.

## 3. 5-Level Difficulty Categorization
Quizzes and questions are categorized into 5 standardized levels:
- 🟢 **Beginner**: Score `< 320`
- 🟡 **Beginner ➜ Medium**: Score `320 - 420`
- 🟠 **Medium**: Score `420 - 520`
- 🔶 **Medium ➜ Hard**: Score `520 - 620`
- 🔴 **Hard / Expert**: Score `620+`

### Confidence Intervals
- `< 10 attempts`: 40% Confidence (Low)
- `10 - 30 attempts`: 75% Confidence (Medium)
- `30+ attempts`: 95% Confidence (High)

## 4. Batch Management Commands
Run these commands to recompute rankings and match scores:

```bash
# 1. Compute content difficulty for quizzes/questions
python manage.py compute_content_difficulty --days 90

# 2. Compute user ability scores
python manage.py compute_user_abilities --days 90

# 3. Compute personalized match scores
python manage.py compute_match_scores --top-n 100
```

## 5. API Endpoints
- `GET /api/intelligence/my-ability/`: Returns current user's ability profile and subject rankings.
- `GET /api/intelligence/learning-path/`: Returns personalized quiz sequence.
- `GET /api/intelligence/progress-insights/`: Returns trends, strengths, weaknesses, and milestones.
- `GET /api/quizzes/<id>/`: Includes the serialized `difficulty_explanation` dictionary.
