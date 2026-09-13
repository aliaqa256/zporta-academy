# Step 16: System Integration, Verification & Final Cleanup

## 1. Objective & Scope
Execute end-to-end integration verification, perform automated regression testing against all endpoints, eliminate deprecated spaghetti legacy code, and finalize the hexagonal architecture backend.

### What is being cleaned / finalized:
- Run the complete characterization test harness across all domains.
- Eliminate dead code, unused imports, duplicate utility scripts, and obsolete legacy view files.
- Audit database queries using `django-debug-toolbar` / query logging to verify zero N+1 query regressions.
- Verify production and local settings with `python manage.py check --deploy`.
- Update documentation and architectural diagrams in `AGENTS.md` and `README.md`.

### What MUST NOT break:
- All platform functionality across frontend (Next.js) and backend (Django REST API).

---

## 2. Pre-flight Checks
- All previous steps (Step 01 to Step 15) must be completed and logged in `backend_rewrite_logs/LOGS.md`.

---

## 3. Planned Changes
- **[DELETE / ARCHIVE]** Obsolete legacy duplicate utility scripts.
- **[MODIFY]** `zporta/settings/base.py`, `local.py`, `production.py` (Clean up obsolete configuration flags).
- **[MODIFY]** `AGENTS.md` (Update domain package layout to reflect Hexagonal Architecture).
- **[MODIFY]** `backend_rewrite_logs/LOGS.md` (Mark all steps completed with performance benchmarks).

---

## 4. Execution Details
1. Run all unit, integration, and characterization test suites.
2. Verify full frontend navigation and dynamic page renders in Next.js.
3. Clean up legacy temporary files and unused imports.
4. Run static type checking / lint checks.

---

## 5. Verification & Tests
- Full test suite run:
  ```bash
  python manage.py test
  pytest
  ```
- Django system check:
  ```bash
  python manage.py check
  ```

---

## 6. Rollback / Backoff Plan
- Final git tag created prior to dead-code removal.
