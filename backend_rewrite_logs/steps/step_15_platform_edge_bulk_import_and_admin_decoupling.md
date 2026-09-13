# Step 15: Platform Edge, Bulk Import & Admin Decoupling

## 1. Objective & Scope
Refactor platform-level edge services including `bulk_import`, `seo`, `pages`, `posts`, `notifications`, and remaining oversized Django admin classes so they strictly interact with domain use cases rather than raw database manipulations.

### What is being cleaned / refactored:
- Extract pure domain models: `ImportBatchEntity`, `ImportValidationReport`, `PageEntity`, `PostEntity`, `NotificationMessage`.
- Extract use cases:
  - `BulkImportCurriculumUseCase` (validates schema, resolves foreign keys, creates courses/lessons/quizzes in a single transactional unit)
  - `PublishNotificationUseCase` (pushes notifications to Firebase / in-app inbox)
  - `GenerateSitemapIndexUseCase`
- Define outbound ports:
  - `BulkImportRepositoryPort`
  - `NotificationDeliveryPort` (Firebase / WebPush)
- Decouple all custom Django Admin actions into thin adapter invocations.

### What MUST NOT break:
- `/api/bulk-import/`, `/api/pages/`, `/api/posts/`, `/api/notifications/`, `/sitemap.xml` endpoints.
- `/administration-zporta-repersentiivie/` custom admin portal URL.

---

## 2. Pre-flight Checks
- Test bulk import and sitemap endpoints.

---

## 3. Planned Changes
- **[NEW]** `bulk_import/application/use_cases/import_curriculum.py`
- **[NEW]** `bulk_import/domain/validation_policy.py`
- **[NEW]** `notifications/application/ports/outbound/notification_port.py`
- **[NEW]** `notifications/adapters/outbound/firebase_adapter.py`
- **[MODIFY]** `bulk_import/views.py`
- **[MODIFY]** `notifications/views.py`
- **[MODIFY]** `pages/views.py`, `posts/views.py`

---

## 4. Execution Details
1. Implement curriculum bulk import validator and use case.
2. Implement Firebase notification delivery adapter.
3. Clean up admin classes across all apps to delegate complex operations to use cases.
4. Verify system check and test suite.

---

## 5. Verification & Tests
- Execute import validation test:
  ```bash
  pytest bulk_import/tests/ notifications/tests/
  ```

---

## 6. Rollback / Backoff Plan
- Reversible via git rollback of individual edge views.
