# Hexagonal Architecture Rewrite Guide for AI Agents (`rewrite_agents.md`)

This document is the authoritative standard and operational guideline for AI coding agents and engineers executing the backend refactoring of **Zporta Academy**.

---

## 1. Core Architecture Vision: Hexagonal (Ports & Adapters)

The backend is being restructured from monolithic, framework-tangled Django spaghetti code into a clean, testable, maintainable **Hexagonal Architecture (Ports and Adapters)**.

```
                  ┌─────────────────────────────────────────────────────────┐
                  │                    INBOUND ADAPTERS                     │
                  │  (REST API Views, Admin Actions, Celery Tasks, CLI)     │
                  └───────────────────────────┬─────────────────────────────┘
                                              │ calls
                                              ▼
                  ┌─────────────────────────────────────────────────────────┐
                  │                 APPLICATION LAYER                       │
                  │  ┌────────────────────┐       ┌──────────────────────┐  │
                  │  │ Inbound Ports/DTOs │       │ Use Case Interactors │  │
                  │  └────────────────────┘       └──────────┬───────────┘  │
                  │                                          │              │
                  │                                          │ orchestrates │
                  │                                          ▼              │
                  │                               ┌──────────────────────┐  │
                  │                               │ Outbound Port (ABCs) │  │
                  │                               └──────────▲───────────┘  │
                  └──────────────────────────────────────────┼──────────────┘
                                                             │
                                              ┌──────────────┴──────────────┐
                                              │ uses / pure rules           │
                                              ▼                             │
                  ┌──────────────────────────────────────────────────────┐  │
                  │                     DOMAIN LAYER                     │  │
                  │  (Entities, Value Objects, Domain Policies, Errors)  │  │
                  │  * ZERO imports from Django, DRF, or 3rd-party libs  │  │
                  └──────────────────────────────────────────────────────┘  │
                                                                            │ implements
                  ┌─────────────────────────────────────────────────────────┴┐
                  │                    OUTBOUND ADAPTERS                     │
                  │  (Django ORM Repositories, AI Gateways, TTS, WeasyPrint) │
                  └──────────────────────────────────────────────────────────┘
```

---

## 2. The 7 Non-Negotiable Golden Rules

1. **Zero Regression Guarantee**:
   - Every public REST endpoint, JSON response contract, URL pattern, and query parameter **must remain 100% backwards compatible**.
   - The Next.js frontend must continue to function without any breaking changes.
2. **Strict Inward Dependency Rule**:
   - `domain/` depends on **nothing external** (no `django.*`, `rest_framework.*`, `requests`, `openai`, etc.).
   - `application/` depends only on `domain/` and its own port definitions.
   - `adapters/` depend on `application/` ports and `domain/`, plus whatever infrastructure library they adapt.
3. **No Business Logic in Views, Serializers, or Admin**:
   - DRF ViewSets / APIViews are strictly **Inbound Adapters** whose sole job is to parse HTTP requests into Use Case Input DTOs, invoke the Use Case, and serialize the Output DTO into an HTTP response.
   - Django admin actions and AJAX endpoints delegate to Use Cases.
4. **All Side Effects & External Services Behind Outbound Ports**:
   - Database queries $\rightarrow$ `*RepositoryPort`
   - AI generation (Gemini, OpenAI, Claude) $\rightarrow$ `LLMProviderPort`
   - Text-to-Speech (Google TTS, ElevenLabs) $\rightarrow$ `TTSProviderPort`
   - Audio stitching (ffmpeg/pydub) $\rightarrow$ `AudioProcessingPort`
   - PDF/Word rendering (WeasyPrint, python-docx) $\rightarrow$ `DocumentRendererPort`
   - Notifications / Emails $\rightarrow$ `NotificationPort` / `EmailSenderPort`
5. **Explicit Composition Root**:
   - Dependency injection is handled centrally in `composition/containers.py` or dedicated factory functions (e.g. `build_submit_quiz_use_case()`).
   - No hidden global service locators or implicit monkey patching.
6. **Error Translation Across Boundaries**:
   - Database/infrastructure exceptions are caught in Outbound Adapters and translated to Domain / Application exceptions.
   - Inbound HTTP Adapters translate Domain / Application exceptions into appropriate HTTP status codes (400, 403, 404, 409, 422).
7. **Step-by-Step Characterization & Verification**:
   - Execute one step at a time as documented in `backend_rewrite_logs/steps/`.
   - Run verification tests before and after modifying any code.
   - Update `backend_rewrite_logs/LOGS.md` after completing each step.

---

## 3. Standard App Directory Structure

For each Django domain app (e.g. `quizzes/`, `courses/`, `dailycast/`, `users/`, `intelligence/`), structure the refactored code as follows:

```
<app_name>/
├── domain/                               # Pure Business Rules (Framework-Agnostic)
│   ├── __init__.py
│   ├── entities.py                       # Dataclasses / Domain Entities
│   ├── value_objects.py                  # Immutable Value Objects (e.g., Score, EloRating)
│   ├── policies.py                       # Pure business calculations & invariants
│   └── exceptions.py                     # App-specific domain exceptions
│
├── application/                          # Use Case Orchestration
│   ├── __init__.py
│   ├── dtos.py                           # Input/Output Data Transfer Objects
│   ├── ports/
│   │   ├── __init__.py
│   │   ├── inbound/                      # Use case interfaces
│   │   └── outbound/                     # Repository & Gateway interfaces (ABCs / Protocols)
│   │       ├── repository_port.py
│   │       └── external_service_port.py
│   └── use_cases/                        # Single-responsibility use cases
│       ├── __init__.py
│       ├── create_item.py
│       └── process_action.py
│
├── adapters/                             # Infrastructure & Delivery
│   ├── __init__.py
│   ├── inbound/
│   │   ├── http/                         # DRF Views & Serializers (Transport only)
│   │   │   ├── views.py
│   │   │   └── serializers.py
│   │   ├── admin/                        # Admin classes & AJAX handlers delegating to use cases
│   │   ├── cli/                          # Django management commands calling use cases
│   │   └── workers/                      # Celery / async tasks calling use cases
│   └── outbound/
│       ├── persistence/                  # Django ORM Repositories implementing ports
│       │   └── django_repository.py
│       └── external/                     # Third-party SDK implementations
│
├── composition/                          # Dependency Injection & Wiring
│   ├── __init__.py
│   └── container.py                      # Factory functions constructing use cases with adapters
│
├── models.py                             # Django ORM database schemas (Persistence only)
├── urls.py                               # URL routing to Inbound HTTP adapters
└── tests/                                # Layer-specific tests
    ├── domain/                           # Pure unit tests (no DB, no mocks)
    ├── application/                      # Use case tests with in-memory fakes
    ├── adapters/                         # Integration tests for ORM repos & HTTP views
    └── e2e/                              # End-to-end API regression tests
```

---

## 4. Python Typing & Clean Code Standards

- **Use Python 3.10+ Type Hints**: All ports, entities, DTOs, and use cases must be strictly typed (`dataclasses`, `Protocol`, `ABC`, `Optional`, `list`, `dict`, `tuple`).
- **Use `@dataclass(frozen=True)`** for Value Objects and DTOs to enforce immutability.
- **Port Definitions with `typing.Protocol` or `abc.ABC`**:
  ```python
  from abc import ABC, abstractmethod

  class QuizRepositoryPort(ABC):
      @abstractmethod
      def get_by_id(self, quiz_id: int) -> Optional[QuizEntity]:
          ...
      @abstractmethod
      def save_attempt(self, attempt: QuizAttemptEntity) -> QuizAttemptEntity:
          ...
  ```
- **Use Cases Receive Ports via `__init__`**:
  ```python
  class SubmitQuizAttemptUseCase:
      def __init__(self, quiz_repo: QuizRepositoryPort, score_policy: ScoringPolicy):
          self._quiz_repo = quiz_repo
          self._score_policy = score_policy

      def execute(self, command: SubmitAttemptCommand) -> AttemptResultDTO:
          # Pure orchestration
          ...
  ```

---

## 5. Workflow Execution Instructions for Agents

1. **Read the Target Step File**: Open and review `backend_rewrite_logs/steps/step_XX_....md`.
2. **Check Pre-requisites**: Run characterization tests to verify current baseline behavior.
3. **Execute Incrementally**:
   - Extract domain entities & value objects.
   - Define outbound ports & DTOs.
   - Implement the use case orchestrator.
   - Implement the ORM repository / external adapter.
   - Refactor the DRF View / Admin action to delegate to the use case via composition root.
4. **Verify Behavior**:
   - Run domain unit tests (instant execution).
   - Run DRF integration tests & check API responses.
   - Run `python manage.py check` to verify Django system integrity.
5. **Update Logs**: Record completed changes and verification results in `backend_rewrite_logs/LOGS.md`.
6. **Ensure Clean Git State**: Keep commits atomic and traceable to the step ID.
