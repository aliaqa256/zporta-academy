# Step 06: Quizzes & Assessment Engine Refactor

## 1. Objective & Scope
Refactor the `quizzes` app into Hexagonal Architecture, isolating quiz attempt grading, question evaluation, answer validation, and score calculation into pure domain logic and application use cases.

### What is being cleaned / refactored:
- Extract pure domain models: `QuizEntity`, `QuestionEntity`, `ChoiceEntity`, `QuizAttemptEntity`, `UserAnswerEntity`, `GradingPolicy`.
- Extract use cases:
  - `GetQuizDetailUseCase`
  - `StartQuizAttemptUseCase`
  - `SubmitQuizAttemptUseCase` (pure grading logic, calculating score, tracking correct/incorrect, generating attempt summary)
  - `GetQuizReviewUseCase`
  - `GetQuestionDifficultyExplanationUseCase`
- Define outbound ports:
  - `QuizRepositoryPort`
  - `QuizAttemptRepositoryPort`
  - `DifficultyServicePort` (connects to intelligence domain without circular coupling)
- Implement ORM persistence adapter in `quizzes/adapters/outbound/persistence/`.
- Clean up heavy `quizzes/views.py` (28KB) and `serializers.py` (29KB).

### What MUST NOT break:
- `/api/quizzes/`, `/api/quizzes/{slug}/`, `/api/quizzes/{id}/attempt/` endpoints.
- `/quizzes/<permalink>/` dynamic permalink view.
- Attempt scoring math and question choice validation.

---

## 2. Pre-flight Checks
- Run quizzes characterization test:
  ```bash
  python manage.py test tests.characterization.test_quizzes_contracts
  ```

---

## 3. Planned Changes
- **[NEW]** `quizzes/domain/entities.py` (QuizEntity, QuestionEntity, ChoiceEntity, AttemptEntity)
- **[NEW]** `quizzes/domain/value_objects.py` (QuestionType, ScorePercentage, DifficultyScore)
- **[NEW]** `quizzes/domain/policies.py` (GradingPolicy, PassingPolicy)
- **[NEW]** `quizzes/domain/exceptions.py` (QuizNotFoundError, InvalidAttemptSubmissionError)
- **[NEW]** `quizzes/application/dtos.py` (QuizDetailDTO, SubmitAttemptCommand, AttemptResultDTO)
- **[NEW]** `quizzes/application/ports/outbound/quiz_repository_port.py`
- **[NEW]** `quizzes/application/ports/outbound/attempt_repository_port.py`
- **[NEW]** `quizzes/application/use_cases/get_quiz_detail.py`
- **[NEW]** `quizzes/application/use_cases/submit_quiz_attempt.py`
- **[NEW]** `quizzes/application/use_cases/get_quiz_history.py`
- **[NEW]** `quizzes/adapters/outbound/persistence/django_quiz_repository.py`
- **[NEW]** `quizzes/composition/container.py`
- **[MODIFY]** `quizzes/views.py` (Delegate to container use cases)
- **[MODIFY]** `quizzes/serializers.py` (Simplify to pure data mapping)

---

## 4. Execution Details
1. Implement pure domain grading rules with comprehensive unit tests for all question types.
2. Implement repository adapter for Quiz and Attempt persistence.
3. Wire use cases through `quizzes/composition/container.py`.
4. Refactor `quizzes/views.py` to invoke use cases.
5. Run characterization suite to guarantee 100% functional equivalence.

---

## 5. Verification & Tests
- Pure unit tests for grading rules and scoring invariants:
  ```bash
  pytest quizzes/tests/domain/ quizzes/tests/application/
  ```
- Characterization tests:
  ```bash
  python manage.py test tests.characterization.test_quizzes_contracts
  ```

---

## 6. Rollback / Backoff Plan
- Reversible via `quizzes/legacy_views.py` route redirection.
