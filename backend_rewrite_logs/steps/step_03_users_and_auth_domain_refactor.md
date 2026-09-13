# Step 03: Users & Authentication Domain Refactor

## 1. Objective & Scope
Refactor the `users` app into Hexagonal Architecture, decoupling domain user identity, authentication, profile management, role policies, and scoring calculations from Django views and models.

### What is being cleaned / refactored:
- Extract pure domain models: `UserEntity`, `UserProfile`, `UserRole` (Student, Teacher, Staff), `LearnerScore`.
- Extract use cases:
  - `AuthenticateUserUseCase`
  - `RegisterUserUseCase`
  - `GetUserProfileUseCase`
  - `UpdateUserProfileUseCase`
  - `CalculateUserScoreUseCase`
  - `GetUserLeaderboardUseCase`
- Define outbound ports:
  - `UserRepositoryPort`
  - `TokenServicePort`
  - `PasswordHasherPort`
- Move Django ORM operations into `users/adapters/outbound/persistence/django_user_repository.py`.
- Slim down `users/views.py` (43KB) into thin HTTP transport adapters that delegate to use cases.
- Split huge `export_views.py` (52KB) into clean use cases and dedicated export adapters.

### What MUST NOT break:
- `/api/users/login/`, `/api/users/register/`, `/api/users/profile/`, `/api/users/leaderboard/` request/response schemas.
- Custom user model schema in PostgreSQL / SQLite.
- Existing tokens, auth headers, and session credentials.

---

## 2. Pre-flight Checks
- Run users characterization test:
  ```bash
  python manage.py test tests.characterization.test_users_contracts
  ```

---

## 3. Planned Changes
- **[NEW]** `users/domain/entities.py` (UserEntity, ProfileEntity)
- **[NEW]** `users/domain/value_objects.py` (Email, UserRole, Level, Score)
- **[NEW]** `users/domain/policies.py` (RolePolicy, ScoreCalculationPolicy)
- **[NEW]** `users/domain/exceptions.py` (UserNotFoundError, InvalidCredentialsError, EmailAlreadyExistsError)
- **[NEW]** `users/application/dtos.py` (LoginDTO, RegisterDTO, UserProfileDTO)
- **[NEW]** `users/application/ports/inbound/auth_use_cases.py`
- **[NEW]** `users/application/ports/outbound/user_repository_port.py`
- **[NEW]** `users/application/ports/outbound/token_service_port.py`
- **[NEW]** `users/application/use_cases/authenticate_user.py`
- **[NEW]** `users/application/use_cases/register_user.py`
- **[NEW]** `users/application/use_cases/get_user_profile.py`
- **[NEW]** `users/application/use_cases/update_user_profile.py`
- **[NEW]** `users/application/use_cases/calculate_user_score.py`
- **[NEW]** `users/adapters/outbound/persistence/django_user_repository.py`
- **[NEW]** `users/adapters/outbound/auth/django_token_service.py`
- **[NEW]** `users/composition/container.py`
- **[MODIFY]** `users/views.py` (Refactor to use container factory and thin handlers)
- **[MODIFY]** `users/serializers.py` (Clean transport mapping only)

---

## 4. Execution Details
1. Implement pure domain entities and scoring calculation rules with unit tests.
2. Implement repository port and Django ORM persistence adapter.
3. Wire use cases in `users/composition/container.py`.
4. Refactor `users/views.py` endpoints to invoke use cases through the container.
5. Verify zero breaking changes via characterization tests.

---

## 5. Verification & Tests
- Run unit tests for domain & use cases (no database needed):
  ```bash
  pytest users/tests/domain/ users/tests/application/
  ```
- Run full characterization suite:
  ```bash
  python manage.py test tests.characterization.test_users_contracts
  ```

---

## 6. Rollback / Backoff Plan
- Keep legacy views aliased or backed up in `users/legacy_views.py` during migration.
- If regression occurs, point `users/urls.py` back to legacy views until fixed.
