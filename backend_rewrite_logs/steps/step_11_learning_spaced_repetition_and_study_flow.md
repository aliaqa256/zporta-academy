# Step 11: Learning, Spaced Repetition & Study Flow

## 1. Objective & Scope
Refactor the `learning` (study queue, spaced repetition intervals) and `notes` apps into Hexagonal Architecture, extracting memory retention math (SM-2 / spaced repetition algorithms) into pure domain policies.

### What is being cleaned / refactored:
- Extract pure domain models: `StudyCardEntity`, `SpacedRepetitionSchedule`, `ReviewRating` (Again, Hard, Good, Easy), `UserNoteEntity`.
- Extract pure domain policies:
  - `SpacedRepetitionPolicy` (calculates next interval, ease factor, and due date based on review rating).
- Extract use cases:
  - `GetDueStudyCardsUseCase` (builds spaced repetition review queue for a student)
  - `SubmitCardReviewUseCase` (applies SM-2 algorithm $\rightarrow$ updates schedule)
  - `CreateOrUpdateUserNoteUseCase`
  - `GetStudentStudyStatsUseCase`
- Define outbound ports:
  - `StudyCardRepositoryPort`
  - `StudyScheduleRepositoryPort`
  - `NoteRepositoryPort`
- Implement Django ORM persistence adapters and slim down `learning/views.py` and `notes/views.py`.

### What MUST NOT break:
- `/api/study/queue/`, `/api/study/submit-review/`, `/api/notes/` endpoints.
- Review intervals and card scheduling state.

---

## 2. Pre-flight Checks
- Verify study queue endpoint response on current database.

---

## 3. Planned Changes
- **[NEW]** `learning/domain/entities.py` (StudyCardEntity, ReviewLogEntity)
- **[NEW]** `learning/domain/policies.py` (SpacedRepetitionPolicy / SM-2 algorithm)
- **[NEW]** `learning/application/dtos.py` (ReviewCardCommand, StudyQueueDTO)
- **[NEW]** `learning/application/ports/outbound/study_repository_port.py`
- **[NEW]** `learning/application/use_cases/get_study_queue.py`
- **[NEW]** `learning/application/use_cases/submit_card_review.py`
- **[NEW]** `learning/adapters/outbound/persistence/django_study_repository.py`
- **[NEW]** `learning/composition/container.py`
- **[MODIFY]** `learning/views.py` (Refactor to delegate to use cases)
- **[MODIFY]** `notes/views.py` (Refactor to delegate to use cases)

---

## 4. Execution Details
1. Implement pure spaced-repetition calculation rules with unit tests.
2. Implement persistence adapters for study queues and user notes.
3. Wire use cases into `learning/composition/container.py`.
4. Refactor HTTP viewsets.
5. Verify zero regression in review schedule calculations.

---

## 5. Verification & Tests
- Unit tests for SM-2 interval calculations:
  ```bash
  pytest learning/tests/
  ```
- Integration test for study review submission.

---

## 6. Rollback / Backoff Plan
- Reversible via `learning/legacy_views.py` route redirection.
