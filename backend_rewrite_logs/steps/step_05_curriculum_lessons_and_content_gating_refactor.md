# Step 05: Curriculum - Lessons & Content Gating Refactor

## 1. Objective & Scope
Refactor the `lessons` app into Hexagonal Architecture, decoupling lesson rendering, teacher configuration gating, progress completion, and content filtering from Django views and ORM queries.

### What is being cleaned / refactored:
- Extract pure domain models: `LessonEntity`, `LessonContent`, `ContentGatingPolicy`, `LessonCompletionEntity`.
- Extract use cases:
  - `GetLessonDetailUseCase` (with gating rules, teacher configs, user permissions)
  - `CompleteLessonUseCase` (marking lesson complete and triggering course progress updates)
  - `GetNextLessonUseCase`
  - `FilterLessonContentUseCase` (role-based / subscription-based content masking)
- Define outbound ports:
  - `LessonRepositoryPort`
  - `TeacherConfigRepositoryPort`
  - `LessonProgressRepositoryPort`
- Move persistence queries from `lessons/views.py` (40KB) into `lessons/adapters/outbound/persistence/`.
- Decouple export hooks (PDF/Word) into outbound port references (detailed in Step 10).

### What MUST NOT break:
- `/api/lessons/`, `/api/lessons/{slug}/`, `/api/lessons/{slug}/complete/` endpoints.
- `/lessons/<permalink>/` dynamic lesson rendering.
- Content gating rules for non-enrolled or free-tier users.

---

## 2. Pre-flight Checks
- Run lessons characterization test:
  ```bash
  python manage.py test tests.characterization.test_lessons_contracts
  ```

---

## 3. Planned Changes
- **[NEW]** `lessons/domain/entities.py` (LessonEntity, LessonSection)
- **[NEW]** `lessons/domain/policies.py` (GatingPolicy, PrerequisitePolicy)
- **[NEW]** `lessons/domain/exceptions.py` (LessonNotFoundError, ContentGatedError)
- **[NEW]** `lessons/application/dtos.py` (LessonDetailDTO, LessonSummaryDTO, CompleteLessonDTO)
- **[NEW]** `lessons/application/ports/outbound/lesson_repository_port.py`
- **[NEW]** `lessons/application/use_cases/get_lesson_detail.py`
- **[NEW]** `lessons/application/use_cases/complete_lesson.py`
- **[NEW]** `lessons/application/use_cases/get_next_lesson.py`
- **[NEW]** `lessons/adapters/outbound/persistence/django_lesson_repository.py`
- **[NEW]** `lessons/composition/container.py`
- **[MODIFY]** `lessons/views.py` (Refactor to clean HTTP transport adapter)
- **[MODIFY]** `lessons/serializers.py` (Map DTOs to DRF output)

---

## 4. Execution Details
1. Implement pure domain entities and gating policies.
2. Implement Django ORM lesson repository.
3. Wire use cases in `lessons/composition/container.py`.
4. Refactor `lessons/views.py` into thin handlers delegating to use cases.
5. Run characterization tests to verify exact payload parity.

---

## 5. Verification & Tests
- Unit tests for gating and completion domain logic:
  ```bash
  pytest lessons/tests/domain/ lessons/tests/application/
  ```
- Characterization integration tests:
  ```bash
  python manage.py test tests.characterization.test_lessons_contracts
  ```

---

## 6. Rollback / Backoff Plan
- Reversible via `lessons/legacy_views.py` delegation switch.
