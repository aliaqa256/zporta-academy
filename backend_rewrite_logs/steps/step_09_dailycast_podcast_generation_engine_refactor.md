# Step 09: DailyCast Podcast Generation Engine Refactor

## 1. Objective & Scope
Refactor the massive `dailycast` app (which contains over 250KB of tangled code across `admin.py`, `views_admin_ajax.py`, `ai_analyzer.py`, and `english_level_analyzer.py`) into clean, modular Hexagonal components.

### What is being cleaned / refactored:
- Extract pure domain models:
  - `DailyCastEpisodeEntity`, `PodcastScriptEntity`, `ScriptSegment` (speaker, timing tags, text, emphasis), `AudioTrackEntity`.
  - `ScriptValidationPolicy` (verifies timing tags `[0:00]`, `[PAUSE]`, character length >1500, required segments).
  - `LearnerProficiencyPolicy` (evaluates CEFR / English levels from study history).
- Extract use cases:
  - `SynthesizeDailyCastScriptUseCase` (fetches learner profile $\rightarrow$ builds LLM prompt $\rightarrow$ validates script)
  - `GenerateEpisodeAudioUseCase` (splits script $\rightarrow$ calls TTS port per speaker $\rightarrow$ stitches audio with intro/outro jingles $\rightarrow$ saves MP3)
  - `PublishDailyCastEpisodeUseCase`
  - `AnalyzeLearnerEnglishLevelUseCase`
  - `GetDailyCastFeedUseCase`
- Define outbound ports:
  - `DailyCastRepositoryPort`
  - `TTSProviderPort` (Google Cloud TTS, ElevenLabs)
  - `AudioStitcherPort` (pydub / ffmpeg)
  - `MediaStoragePort` (Local `MEDIA_ROOT/podcasts/` / S3)
- Break down monolithic files:
  - Dissect `admin.py` (91KB) into separate admin descriptors delegating to use cases.
  - Dissect `views_admin_ajax.py` (54KB) into thin HTTP transport endpoints calling use cases.
  - Dissect `ai_analyzer.py` (48KB) into domain policies and application use cases.

### What MUST NOT break:
- `/api/dailycast/episodes/`, `/api/dailycast/generate/`, `/api/admin/ajax/dailycast/` endpoints.
- Admin interactive podcast generator UI.
- Google TTS voice configurations (`ja-JP-Neural2-B`, `ja-JP-Wavenet-*`, `en-US-Neural2-*`).
- Audio file storage paths in `MEDIA_ROOT/podcasts/`.

---

## 2. Pre-flight Checks
- Run dailycast characterization & audio test:
  ```bash
  python test_dailycast.py
  python test_simple_podcast.py
  ```

---

## 3. Planned Changes
- **[NEW]** `dailycast/domain/entities.py` (EpisodeEntity, ScriptEntity, AudioTrackEntity)
- **[NEW]** `dailycast/domain/policies.py` (ScriptValidationPolicy, ProficiencyPolicy)
- **[NEW]** `dailycast/domain/exceptions.py` (InvalidScriptError, AudioSynthesisError)
- **[NEW]** `dailycast/application/dtos.py` (GenerateScriptCommand, SynthesizeAudioCommand, EpisodeDTO)
- **[NEW]** `dailycast/application/ports/outbound/dailycast_repository_port.py`
- **[NEW]** `dailycast/application/ports/outbound/tts_provider_port.py`
- **[NEW]** `dailycast/application/ports/outbound/audio_stitcher_port.py`
- **[NEW]** `dailycast/application/ports/outbound/media_storage_port.py`
- **[NEW]** `dailycast/application/use_cases/synthesize_script.py`
- **[NEW]** `dailycast/application/use_cases/generate_audio.py`
- **[NEW]** `dailycast/application/use_cases/publish_episode.py`
- **[NEW]** `dailycast/adapters/outbound/tts/google_tts_adapter.py`
- **[NEW]** `dailycast/adapters/outbound/tts/elevenlabs_tts_adapter.py`
- **[NEW]** `dailycast/adapters/outbound/audio/pydub_stitcher_adapter.py`
- **[NEW]** `dailycast/adapters/outbound/persistence/django_dailycast_repository.py`
- **[NEW]** `dailycast/composition/container.py`
- **[MODIFY]** `dailycast/views_api.py` (Refactor to use container)
- **[MODIFY]** `dailycast/views_admin_ajax.py` (Refactor to use container)
- **[MODIFY]** `dailycast/admin.py` (Refactor to delegate actions to use cases)

---

## 4. Execution Details
1. Implement pure script validation and segment parsing in domain.
2. Implement TTS adapters (Google TTS & ElevenLabs) satisfying `TTSProviderPort`.
3. Implement `PydubStitcherAdapter` satisfying `AudioStitcherPort`.
4. Assemble `GenerateEpisodeAudioUseCase` and test with mock audio fixtures.
5. Refactor AJAX admin views and public REST API to call use cases.
6. Verify output audio format, metadata, and duration against baseline.

---

## 5. Verification & Tests
- Unit tests for script validation & audio segment orchestrator:
  ```bash
  pytest dailycast/tests/
  ```
- End-to-end podcast generation smoke test:
  ```bash
  python test_dailycast.py
  ```

---

## 6. Rollback / Backoff Plan
- Keep legacy services available as fallback until new audio synthesis is verified with live Google TTS credentials.
