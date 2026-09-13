# Step 01: Architecture Foundation & Shared Kernel

## 1. Objective & Scope
Establish the shared core abstractions and foundational building blocks needed across all hexagonal domains in `zporta_academy_backend`.

### What is being cleaned / created:
- Create `core/shared_kernel/` containing:
  - Base Domain Entity & Value Object base classes / type utilities (`domain/base_entity.py`, `domain/value_object.py`).
  - Standard Result / Either monad types (`Result[T, E]`, `Success`, `Failure`) to prevent unchecked exceptions across architectural boundaries.
  - Base Inbound/Outbound Port abstract interfaces (`ports/base_repository.py`, `ports/clock_port.py`, `ports/id_generator.py`).
  - Domain base exceptions (`domain/exceptions.py`).
  - Standard pagination, filtering, and sort DTOs.
  - Standard composition container patterns.

### What MUST NOT break:
- No existing Django apps are modified yet.
- Zero changes to database tables or existing endpoints.

---

## 2. Pre-flight Checks
- Verify Django system check passes:
  ```bash
  cd zporta_academy_backend
  python manage.py check
  ```

---

## 3. Planned Changes
- **[NEW]** `zporta_academy_backend/core/__init__.py`
- **[NEW]** `zporta_academy_backend/core/shared_kernel/domain/base_entity.py`
- **[NEW]** `zporta_academy_backend/core/shared_kernel/domain/value_objects.py`
- **[NEW]** `zporta_academy_backend/core/shared_kernel/domain/result.py`
- **[NEW]** `zporta_academy_backend/core/shared_kernel/domain/exceptions.py`
- **[NEW]** `zporta_academy_backend/core/shared_kernel/application/ports/clock_port.py`
- **[NEW]** `zporta_academy_backend/core/shared_kernel/application/ports/base_repository.py`
- **[NEW]** `zporta_academy_backend/core/shared_kernel/application/dtos/pagination.py`
- **[NEW]** `zporta_academy_backend/core/shared_kernel/adapters/system_clock.py`
- **[NEW]** `zporta_academy_backend/core/shared_kernel/tests/test_result.py`
- **[NEW]** `zporta_academy_backend/core/shared_kernel/tests/test_entities.py`

---

## 4. Execution Details
1. Implement pure python Result type with `.is_success`, `.is_failure`, `.value`, `.error`.
2. Implement Domain Entity dataclass base with immutable identity and equality by ID.
3. Implement standard BaseRepository Port with generic CRUD typing.
4. Implement SystemClockPort with real and mock implementations for deterministic testing.
5. Add unit tests for shared kernel components in pure Python (0 ms execution).

---

## 5. Verification & Tests
- Execute shared kernel pure unit tests:
  ```bash
  pytest core/shared_kernel/tests/
  ```
- Run `python manage.py check` to ensure zero import conflicts.

---

## 6. Rollback / Backoff Plan
- If issues occur, remove the `core/` package. No external dependencies are touched.
