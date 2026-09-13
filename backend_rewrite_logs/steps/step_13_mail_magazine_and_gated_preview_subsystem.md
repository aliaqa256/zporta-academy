# Step 13: Mail Magazine & Gated Preview Subsystem Refactor

## 1. Objective & Scope
Refactor the `mailmagazine` app into Hexagonal Architecture, decoupling subscriber management, issue publishing, gated preview truncation policies, and email sending.

### What is being cleaned / refactored:
- Extract pure domain models: `MailIssueEntity`, `SubscriberEntity`, `GatedPreviewPolicy`, `DispatchBatch`.
- Extract pure domain policies:
  - `GatedPreviewPolicy` (truncates issue content for non-subscribers with configurable preview length and teaser cards).
- Extract use cases:
  - `GetMailIssueDetailUseCase` (applies gating policy based on subscription status)
  - `SubscribeToMailMagazineUseCase`
  - `PublishAndDispatchIssueUseCase` (schedules bulk email delivery)
  - `GetTeacherMailMagazineIssuesUseCase`
- Define outbound ports:
  - `MailMagazineRepositoryPort`
  - `EmailSenderPort`
  - `TemplateRendererPort`
- Implement ORM repository adapters and email sender adapter.

### What MUST NOT break:
- `/api/mailmagazine/issues/`, `/api/mailmagazine/subscribe/`, `/api/mailmagazine/issues/{id}/` endpoints.
- Subscriber verification tokens and unsubscribe links.

---

## 2. Pre-flight Checks
- Test mailmagazine issues endpoint and preview truncation.

---

## 3. Planned Changes
- **[NEW]** `mailmagazine/domain/entities.py` (MailIssueEntity, SubscriberEntity)
- **[NEW]** `mailmagazine/domain/policies.py` (GatedPreviewPolicy)
- **[NEW]** `mailmagazine/application/dtos.py` (IssueDetailDTO, SubscribeCommand)
- **[NEW]** `mailmagazine/application/ports/outbound/mail_repository_port.py`
- **[NEW]** `mailmagazine/application/ports/outbound/email_sender_port.py`
- **[NEW]** `mailmagazine/application/use_cases/get_issue_detail.py`
- **[NEW]** `mailmagazine/application/use_cases/subscribe_user.py`
- **[NEW]** `mailmagazine/application/use_cases/dispatch_issue.py`
- **[NEW]** `mailmagazine/adapters/outbound/persistence/django_mail_repository.py`
- **[NEW]** `mailmagazine/adapters/outbound/email/smtp_email_adapter.py`
- **[NEW]** `mailmagazine/composition/container.py`
- **[MODIFY]** `mailmagazine/views.py` (Delegate to container use cases)

---

## 4. Execution Details
1. Implement pure domain entities and gating policies with unit tests.
2. Implement repository port and email sender adapter.
3. Wire use cases into `mailmagazine/composition/container.py`.
4. Refactor `mailmagazine/views.py` to thin handlers.
5. Verify zero regression.

---

## 5. Verification & Tests
- Unit tests for gated preview logic:
  ```bash
  pytest mailmagazine/tests/
  ```

---

## 6. Rollback / Backoff Plan
- Reversible via `mailmagazine/legacy_views.py` backup.
