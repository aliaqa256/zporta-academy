# Step 08: AI Core & Multi-Provider LLM Gateway

## 1. Objective & Scope
Refactor the `ai_core` app into a clean Hexagonal Gateway with outbound ports and provider adapters, providing a unified, resilient interface for LLM operations (Gemini, OpenAI, Claude) with automated fallback, cost logging, and structured generation.

### What is being cleaned / refactored:
- Extract domain models: `PromptTemplateEntity`, `LLMRequest`, `LLMResponse`, `ModelProvider` (Gemini, OpenAI, Anthropic), `TokenUsage`, `CostEstimate`.
- Extract use cases:
  - `GenerateStructuredInsightUseCase`
  - `SelectOptimalLLMProviderUseCase` (balancing cost, speed, and capability)
  - `LogAndTrackLLMUsageUseCase`
- Define outbound ports:
  - `LLMProviderPort` (abstract interface for chat/completion/structured output)
  - `PromptTemplateRepositoryPort`
  - `AIUsageLogRepositoryPort`
- Implement outbound adapters:
  - `GeminiProviderAdapter` (Google GenAI / Gemini 1.5 Flash)
  - `OpenAIProviderAdapter` (GPT-4o Mini)
  - `AnthropicProviderAdapter` (Claude 3.5 Haiku)
  - `CompositeResilientLLMAdapter` (implements automatic fallback if primary provider fails or rate limits)

### What MUST NOT break:
- Existing AI prompt templates in the database.
- AI provider configuration models and usage cost metrics.

---

## 2. Pre-flight Checks
- Test LLM connectivity and fallback configuration:
  ```bash
  python test_llm_selector.py
  ```

---

## 3. Planned Changes
- **[NEW]** `ai_core/domain/entities.py` (LLMRequest, LLMResponse, ModelInfo)
- **[NEW]** `ai_core/domain/exceptions.py` (ProviderUnavailableError, QuotaExceededError, OutputParsingError)
- **[NEW]** `ai_core/application/ports/outbound/llm_provider_port.py`
- **[NEW]** `ai_core/application/ports/outbound/usage_log_port.py`
- **[NEW]** `ai_core/application/use_cases/generate_completion.py`
- **[NEW]** `ai_core/adapters/outbound/providers/gemini_adapter.py`
- **[NEW]** `ai_core/adapters/outbound/providers/openai_adapter.py`
- **[NEW]** `ai_core/adapters/outbound/providers/anthropic_adapter.py`
- **[NEW]** `ai_core/adapters/outbound/providers/resilient_fallback_gateway.py`
- **[NEW]** `ai_core/adapters/outbound/persistence/django_ai_repository.py`
- **[NEW]** `ai_core/composition/container.py`
- **[MODIFY]** `ai_core/services.py` (Refactor to delegate to container)

---

## 4. Execution Details
1. Define pure `LLMProviderPort` interface with typed DTOs.
2. Implement isolated provider adapters with unified error handling.
3. Build `ResilientFallbackGateway` with timeout handling and circuit breaking.
4. Implement Django repository adapter for token & cost logging.
5. Provide composition root for dependency injection across the codebase.

---

## 5. Verification & Tests
- Mocked unit tests for provider adapters & fallback switching:
  ```bash
  pytest ai_core/tests/
  ```
- Live connectivity smoke test for configured API keys.

---

## 6. Rollback / Backoff Plan
- Reversible via `ai_core/services.py` legacy interface wrappers.
