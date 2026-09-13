# Hexagonal Architecture Rewrite Guide for AI Agents (`rewrite_agents.md`)

Please refer to the authoritative specification in [backend_rewrite_logs/rewrite_agents.md](file:///home/aliaqa/zporta-academy/backend_rewrite_logs/rewrite_agents.md).

---

## Quick Reference Summary

- **Architecture**: Hexagonal (Ports and Adapters).
- **Core Principle**: Dependency direction is always inward (`Adapters` $\rightarrow$ `Application Use Cases` $\rightarrow$ `Domain Entities/Policies`).
- **Domain Layer**: 100% framework-agnostic. No Django, DRF, or third-party imports.
- **Application Layer**: Use case orchestrators, Inbound/Outbound Port contracts (Protocols/ABCs), input/output DTOs.
- **Adapters Layer**: Inbound (DRF ViewSets, Admin actions, CLI commands, Celery tasks) & Outbound (Django ORM repositories, AI LLM clients, TTS synthesis, WeasyPrint PDF engines).
- **Zero Regression**: Preserves 100% of existing API endpoints, URL routes, JSON serialization schemas, and database tables.
- **Step Roadmap**: Step-by-step documentation located in [backend_rewrite_logs/steps/](file:///home/aliaqa/zporta-academy/backend_rewrite_logs/steps/).
- **Activity Log**: Keep [backend_rewrite_logs/LOGS.md](file:///home/aliaqa/zporta-academy/backend_rewrite_logs/LOGS.md) updated after completing each step.
