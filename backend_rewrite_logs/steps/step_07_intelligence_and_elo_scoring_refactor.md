# Step 07: Intelligence & ELO Scoring Analytics Refactor

## 1. Objective & Scope
Refactor the `intelligence` and `analytics` apps into Hexagonal Architecture, extracting the mathematical algorithms for ELO difficulty calculation, learner ability updates, and Zone of Proximal Development (ZPD) match scoring into pure domain policies.

### What is being cleaned / refactored:
- Extract pure domain models: `EloRating` (0-1000 scale), `DifficultyLevelPolicy` (5 discrete tiers: 🟢 `<320`, 🟡 `320-420`, 🟠 `420-520`, 🔶 `520-620`, 🔴 `620+`), `ZpdMatchScorePolicy`, `AbilityUpdatePolicy`.
- Extract use cases:
  - `CalculateEloUpdateUseCase` (computes K-factor, expected vs actual score, and new ratings)
  - `ComputeBatchContentDifficultyUseCase` (offline/batch computation for quizzes and questions)
  - `ComputeBatchUserAbilitiesUseCase` (offline/batch computation for learner profiles)
  - `GenerateFeedRecommendationsUseCase` (ZPD match scoring for personalized feed)
  - `GetLearnerAbilityOverviewUseCase`
- Define outbound ports:
  - `AbilityProfileRepositoryPort`
  - `DifficultyProfileRepositoryPort`
  - `MatchScoreRepositoryPort`
- Move management commands into inbound CLI adapters that call use cases.
- Slim down `intelligence/views.py` into clean HTTP transport adapters.

### What MUST NOT break:
- `/api/intelligence/recommendations/`, `/api/intelligence/user-abilities/` endpoints.
- Mathematical consistency with previous ELO scores and difficulty classifications.
- Django management commands (`compute_user_abilities`, `compute_content_difficulty`, `compute_match_scores`).

---

## 2. Pre-flight Checks
- Run intelligence characterization test:
  ```bash
  python manage.py test tests.characterization.test_intelligence_contracts
  ```

---

## 3. Planned Changes
- **[NEW]** `intelligence/domain/entities.py` (UserAbilityEntity, ContentDifficultyEntity, MatchScoreEntity)
- **[NEW]** `intelligence/domain/value_objects.py` (EloScore, DifficultyBand, ZpdScore)
- **[NEW]** `intelligence/domain/policies.py` (EloCalculationPolicy, ZpdScoringPolicy, LevelClassificationPolicy)
- **[NEW]** `intelligence/application/dtos.py` (LearnerAbilityDTO, ContentDifficultyDTO, MatchScoreDTO)
- **[NEW]** `intelligence/application/ports/outbound/ability_repository_port.py`
- **[NEW]** `intelligence/application/ports/outbound/difficulty_repository_port.py`
- **[NEW]** `intelligence/application/use_cases/calculate_elo_update.py`
- **[NEW]** `intelligence/application/use_cases/compute_batch_difficulty.py`
- **[NEW]** `intelligence/application/use_cases/generate_feed_recommendations.py`
- **[NEW]** `intelligence/adapters/outbound/persistence/django_intelligence_repository.py`
- **[NEW]** `intelligence/composition/container.py`
- **[MODIFY]** `intelligence/views.py` (Delegate to container use cases)
- **[MODIFY]** `intelligence/management/commands/*.py` (Adapt to invoke use cases)

---

## 4. Execution Details
1. Implement pure ELO math and ZPD ranking domain logic with 100% test coverage.
2. Implement Django ORM persistence adapters for ability, difficulty, and match score tables.
3. Wire use cases through `intelligence/composition/container.py`.
4. Refactor views and CLI commands to call use cases.
5. Verify matching calculation outputs with baseline dataset.

---

## 5. Verification & Tests
- Pure unit tests for ELO formulas & ZPD ranking:
  ```bash
  pytest intelligence/tests/domain/ intelligence/tests/application/
  ```
- Command run verification:
  ```bash
  python manage.py compute_content_difficulty --dry-run
  ```

---

## 6. Rollback / Backoff Plan
- Keep existing computation utilities as fallback until verified against live datasets.
