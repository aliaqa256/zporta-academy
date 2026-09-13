# Step 12: Payments, Enrollment & Subscription Gating

## 1. Objective & Scope
Refactor `payments` and `enrollment` into a clean Hexagonal architecture, decoupling payment gateway processing, transaction verification, course enrollment grants, and access gating.

### What is being cleaned / refactored:
- Extract pure domain models: `EnrollmentEntity`, `PaymentTransactionEntity`, `EnrollmentAccessPolicy`, `SubscriptionPlanEntity`.
- Extract use cases:
  - `EnrollUserInCourseUseCase` (verifies eligibility, grants access, triggers welcome notifications)
  - `ProcessPaymentCheckoutUseCase` (validates amount, calls payment gateway port)
  - `VerifyPaymentWebhookUseCase` (idempotent webhook processing)
  - `CheckUserCourseAccessUseCase`
- Define outbound ports:
  - `EnrollmentRepositoryPort`
  - `PaymentTransactionRepositoryPort`
  - `PaymentGatewayPort` (Stripe / custom gateway abstraction)
- Implement ORM persistence adapters and slim down `enrollment/views.py` and `payments/views.py`.

### What MUST NOT break:
- `/api/enrollment/`, `/api/payments/` endpoints.
- Existing enrollment records and student course access checks.

---

## 2. Pre-flight Checks
- Verify existing enrollment records and test access check endpoint.

---

## 3. Planned Changes
- **[NEW]** `enrollment/domain/entities.py` (EnrollmentEntity, AccessGrant)
- **[NEW]** `enrollment/domain/policies.py` (AccessPolicy)
- **[NEW]** `payments/domain/entities.py` (PaymentOrder, Transaction)
- **[NEW]** `payments/application/ports/outbound/payment_gateway_port.py`
- **[NEW]** `enrollment/application/ports/outbound/enrollment_repository_port.py`
- **[NEW]** `enrollment/application/use_cases/enroll_user.py`
- **[NEW]** `payments/application/use_cases/process_payment.py`
- **[NEW]** `enrollment/adapters/outbound/persistence/django_enrollment_repository.py`
- **[NEW]** `payments/adapters/outbound/gateways/stripe_gateway_adapter.py`
- **[MODIFY]** `enrollment/views.py` (Refactor to use container)
- **[MODIFY]** `payments/views.py` (Refactor to use container)

---

## 4. Execution Details
1. Implement pure domain access policies.
2. Implement payment gateway port and Stripe adapter.
3. Wire use cases into composition root.
4. Refactor views and serializers to thin HTTP handlers.
5. Verify zero regression.

---

## 5. Verification & Tests
- Unit tests for enrollment and payment policies:
  ```bash
  pytest enrollment/tests/ payments/tests/
  ```

---

## 6. Rollback / Backoff Plan
- Reversible via legacy view wrappers.
