---
name: podcast-engine
description: Complete guide and workflow for DailyCast and interactive podcast generation, LLM prompt engineering, Google TTS synthesis, and audio stitching.
---

# Podcast Engine & DailyCast Generation Guide

## 1. Overview
The DailyCast engine generates personalized, spaced-repetition English learning audio episodes for users based on their learning history, weak concepts, and ability profile.

## 2. Audio Generation Pipeline
```
[User Ability Profile + Weak Concepts]
                  ↓
[LLM Script Generation (Gemini Flash / GPT-4o-Mini)]
                  ↓
[Script Validation (>1500 chars, Section Tags)]
                  ↓
[Google Cloud TTS Synthesis (ja-JP / en-US)]
                  ↓
[Audio Stitching (pydub / ffmpeg: Intro + Voice + Outro)]
                  ↓
[Save MP3 to MEDIA_ROOT/podcasts/ or S3]
```

## 3. LLM Prompt Template & Tags
The LLM generates scripts containing pacing and emphasis markers:
- `[0:00]`, `[0:30]`, `[1:00]`, `[3:30]`, `[4:30]`: Section timestamps.
- `[PAUSE]`: Inserts a short breath pause (~500ms).
- `[EMPHASIS]`: Highlights stressed terminology or pronunciation cues.
- `[SLOWER]`: Pacing directive for pronunciation breakdown.

### Script Validation Checklist
- Minimum script length: >1500 characters.
- Required sections: Greeting & progress summary, Focus introduction, Mini-lesson explanation, Quick practice section, Encouragement & closing.
- Non-repetitive check.

## 4. Google Cloud TTS Voice Reference
- **Japanese Explanations & Host**: `ja-JP-Neural2-B` (Male) or `ja-JP-Neural2-C` (Female).
- **English Practice & Audio**: `en-US-Neural2-F` (Female) or `en-US-Neural2-J` (Male).
- **Audio Output Settings**: MP3 format, 24kHz sampling rate, natural pitch and speaking rate adjustments.

## 5. Storage Fallback
When AWS S3 storage is disabled, podcast files are saved locally under:
- Directory: `settings.MEDIA_ROOT / 'podcasts' / 'episodes' /`
- Served via URL path: `/media/podcasts/episodes/<filename>.mp3`
