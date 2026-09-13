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

## 2. Completeness & Scope Guarantee

Upon completing the 16 steps defined in `backend_rewrite_logs/steps/`:
1. **Every single domain** (Users, Courses, Lessons, Quizzes, Intelligence/ELO, AI Core, DailyCast, WeasyPrint Media, Learning/SM-2, Payments, MailMagazine, Feed/Social, Bulk Import, Admin, SEO) is 100% cleanly decoupled into Hexagonal boundaries.
2. **All spaghetti monoliths are dismantled**: Monolithic 91KB admin files, 54KB AJAX views, 52KB export views, and 48KB analyzer files are broken down into single-responsibility use cases, pure domain policies, and thin adapters.
3. **Dead code & duplicate scripts are pruned**: Obsolete scripts and duplicate logic are safely eliminated with characterization test validation.
4. **No further restructuring will be required**: The codebase will be modular, testable in milliseconds with pure Python fakes, and maintainable for long-term production scaling.

---

## 3. Mandatory Pre-Change & Post-Change Validation Protocol

Every AI agent and developer **MUST** follow this strict verification protocol before and after making code modifications in any step:

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                    PRE-CHANGE VALIDATION GATE (MANDATORY)                     │
├───────────────────────────────────────────────────────────────────────────────┤
│ 1. Run Django System Check:                                                   │
│    python manage.py check                                                     │
│ 2. Run Domain Characterization Test Suite:                                    │
│    python manage.py test tests.characterization.<domain_test_file>               │
│ 3. Record Baseline: Verify status code, response schema, and query behavior.   │
└───────────────────────────────────────┬───────────────────────────────────────┘
                                        │
                                        ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                         APPLY HEXAGONAL REFACTORING                           │
│  Extract Domain Rules -> Define Ports/DTOs -> Implement Use Case ->           │
│  Implement Adapters -> Wire in Container -> Slim Down Views / Admin           │
└───────────────────────────────────────┬───────────────────────────────────────┘
                                        │
                                        ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│                    POST-CHANGE VALIDATION GATE (MANDATORY)                    │
├───────────────────────────────────────────────────────────────────────────────┤
│ 1. Run Pure Domain Unit Tests (0ms execution, zero DB):                        │
│    pytest <app_name>/tests/domain/                                            │
│ 2. Run Application Use Case Tests (using in-memory fakes):                    │
│    pytest <app_name>/tests/application/                                       │
│ 3. Run Outbound Adapter Integration Tests:                                    │
│    pytest <app_name>/tests/adapters/                                          │
│ 4. Run Characterization & Contract Regression Suite:                          │
│    python manage.py test tests.characterization                               │
│ 5. Run Django System & Migration Check:                                       │
│    python manage.py check && python manage.py makemigrations --check --dry-run │
│ 6. Update LOGS.md with test output evidence and mark step status.             │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. The 7 Non-Negotiable Golden Rules

1. **Zero Regression Guarantee**:
   - Every public REST endpoint, JSON response contract, URL pattern, and query parameter **must remain 100% backwards compatible**.
   - The Next.js frontend must continue to function seamlessly without any breaking changes.
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
   - Dependency injection is handled centrally in `composition/container.py` or dedicated factory functions (e.g. `build_submit_quiz_use_case()`).
   - No hidden global service locators or implicit monkey patching.
6. **Error Translation Across Boundaries**:
   - Database/infrastructure exceptions are caught in Outbound Adapters and translated to Domain / Application exceptions.
   - Inbound HTTP Adapters translate Domain / Application exceptions into appropriate HTTP status codes (400, 403, 404, 409, 422).
7. **Step-by-Step Characterization & Verification**:
   - Execute one step at a time as documented in `backend_rewrite_logs/steps/`.
   - Never skip the Pre-Change or Post-Change validation gates.
   - Update `backend_rewrite_logs/LOGS.md` after completing each step.

---

## 5. Standard App Directory Structure

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
