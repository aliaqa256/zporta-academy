# Step 02: Characterization & Safety Test Harness

## 1. Objective & Scope
Establish automated characterization and contract tests for all critical existing endpoints before refactoring application code. This creates a concrete safety net ensuring zero regressions during domain rewrites.

### Endpoints Covered by Characterization Harness:
- **Auth & Users**: `/api/users/login/`, `/api/users/register/`, `/api/users/profile/`, `/api/users/leaderboard/`
- **Courses**: `/api/courses/`, `/api/courses/{slug}/`, `/api/courses/{slug}/progress/`
- **Lessons**: `/api/lessons/`, `/api/lessons/{slug}/`, `/api/lessons/{slug}/export/pdf/`
- **Quizzes**: `/api/quizzes/`, `/api/quizzes/{slug}/`, `/api/quizzes/{id}/attempt/`
- **Intelligence**: `/api/intelligence/recommendations/`, `/api/intelligence/user-abilities/`
- **DailyCast**: `/api/dailycast/episodes/`, `/api/dailycast/generate/`
- **Learning**: `/api/study/queue/`, `/api/study/submit-review/`
- **Mail Magazine**: `/api/mailmagazine/issues/`, `/api/mailmagazine/subscribe/`

### What MUST NOT break:
- All characterization assertions represent the exact live contract expected by the Next.js frontend.

---

## 2. Pre-flight Checks
- Verify local database is migrated and accessible.
- Verify test runner works:
  ```bash
  python manage.py test --keepdb
  ```

---

## 3. Planned Changes
- **[NEW]** `zporta_academy_backend/tests/characterization/__init__.py`
- **[NEW]** `zporta_academy_backend/tests/characterization/test_users_contracts.py`
- **[NEW]** `zporta_academy_backend/tests/characterization/test_courses_contracts.py`
- **[NEW]** `zporta_academy_backend/tests/characterization/test_lessons_contracts.py`
- **[NEW]** `zporta_academy_backend/tests/characterization/test_quizzes_contracts.py`
- **[NEW]** `zporta_academy_backend/tests/characterization/test_intelligence_contracts.py`
- **[NEW]** `zporta_academy_backend/tests/characterization/test_dailycast_contracts.py`
- **[NEW]** `zporta_academy_backend/tests/characterization/fixtures/standard_test_data.py`

---

## 4. Execution Details
1. Set up standard test fixtures for users (student, teacher, admin), courses, lessons, and quizzes.
2. Record exact JSON response keys, status codes, and error payloads for each endpoint.
3. Write characterization test cases asserting exact schema matching and invariant behaviors.

---

## 5. Verification & Tests
- Execute characterization test suite:
  ```bash
  python manage.py test tests.characterization
  ```
- All tests must pass on the current legacy codebase before proceeding to Step 03.

---

## 6. Rollback / Backoff Plan
- If tests reveal existing broken legacy paths, document the edge cases and fix test fixtures without altering business logic.
