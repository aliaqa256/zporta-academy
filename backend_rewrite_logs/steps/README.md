# Backend Restructure Steps

This directory contains individual step files (`step_1.md`, `step_2.md`, ..., `step_n.md`) defining the exact plan, implementation details, automated tests, and rollback procedures for each rewrite phase.

---

## Step File Template Reference

Each step file will follow this structure:
```markdown
# Step X: [Step Name]

## 1. Objective & Scope
- What is being cleaned / refactored.
- What MUST NOT break (API contracts, DB schemas).

## 2. Pre-flight Checks
- Baseline tests to run before modifying code.

## 3. Planned Changes
- Files to modify, delete, or create.
- Architectural design / pattern improvements.

## 4. Execution Details
- Step-by-step diff/code updates.

## 5. Verification & Tests
- Automated test runs & manual curl/API checks.

## 6. Rollback / Backoff Plan
- Instructions to revert safely if issues arise.
```
