# Step 04: Curriculum - Courses & Subjects Refactor

## 1. Objective & Scope
Refactor the `courses` and `subjects` apps into Hexagonal Architecture, decoupling course catalog retrieval, syllabus structuring, prerequisite validation, and course progress from Django models and views.

### What is being cleaned / refactored:
- Extract pure domain models: `CourseEntity`, `SubjectEntity`, `CourseSyllabus`, `CoursePrerequisitesPolicy`, `CourseProgressEntity`.
- Extract use cases:
  - `GetCourseCatalogUseCase` (with filtering, subject/tag search, pagination)
  - `GetCourseDetailUseCase` (with syllabus & dynamic permalinks)
  - `CalculateCourseProgressUseCase`
  - `EnrollStudentInCourseUseCase`
  - `ManageCoursePrerequisitesUseCase`
- Define outbound ports:
  - `CourseRepositoryPort`
  - `SubjectRepositoryPort`
  - `CourseProgressRepositoryPort`
- Implement ORM persistence adapters in `courses/adapters/outbound/persistence/`.
- Slim down `courses/views.py` (20KB) to thin HTTP adapters.

### What MUST NOT break:
- `/api/courses/`, `/api/courses/{slug}/`, `/api/courses/{slug}/progress/`, `/api/subjects/` endpoints.
- Permalink resolution for `/courses/<permalink>/` dynamic view.
- Course and Subject database tables and relationships.

---

## 2. Pre-flight Checks
- Run courses characterization test:
  ```bash
  python manage.py test tests.characterization.test_courses_contracts
  ```

---

## 3. Planned Changes
- **[NEW]** `courses/domain/entities.py` (CourseEntity, SubjectEntity, ModuleEntity)
- **[NEW]** `courses/domain/value_objects.py` (CourseSlug, DifficultyLevel, Price)
- **[NEW]** `courses/domain/policies.py` (PrerequisitePolicy, CourseCompletionPolicy)
- **[NEW]** `courses/domain/exceptions.py` (CourseNotFoundError, PrerequisiteNotMetError)
- **[NEW]** `courses/application/dtos.py` (CourseSummaryDTO, CourseDetailDTO, CourseProgressDTO)
- **[NEW]** `courses/application/ports/outbound/course_repository_port.py`
- **[NEW]** `courses/application/ports/outbound/subject_repository_port.py`
- **[NEW]** `courses/application/use_cases/get_course_catalog.py`
- **[NEW]** `courses/application/use_cases/get_course_detail.py`
- **[NEW]** `courses/application/use_cases/get_course_progress.py`
- **[NEW]** `courses/adapters/outbound/persistence/django_course_repository.py`
- **[NEW]** `courses/composition/container.py`
- **[MODIFY]** `courses/views.py` (Delegate to container use cases)
- **[MODIFY]** `courses/serializers.py` (Pure transport serialization)

---

## 4. Execution Details
1. Define pure course and subject entities with domain policies.
2. Implement Django ORM course repository mapping ORM models to domain entities and vice-versa.
3. Wire use cases inside `courses/composition/container.py`.
4. Update DRF viewsets to invoke use cases.
5. Verify zero API regression.

---

## 5. Verification & Tests
- Execute pure unit tests:
  ```bash
  pytest courses/tests/domain/ courses/tests/application/
  ```
- Run characterization tests:
  ```bash
  python manage.py test tests.characterization.test_courses_contracts
  ```

---

## 6. Rollback / Backoff Plan
- Keep `courses/legacy_views.py` as backup fallback. If any query optimization fails, revert URL route immediately.
