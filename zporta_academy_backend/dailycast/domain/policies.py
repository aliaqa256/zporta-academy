"""
DailyCast Domain Policies.
"""
import re
from math import ceil
from typing import Any, Dict, List, Tuple
from dailycast.domain.entities import DailyPodcastEntity, ScriptSegment
from dailycast.domain.value_objects import OutputFormat, PodcastStatus


class ScriptValidationPolicy:
    """Policy verifying script format, word count, timing tags, and question structure."""

    @staticmethod
    def validate_script(script_text: str, min_words: int = 50) -> Tuple[bool, List[str]]:
        errors = []
        if not script_text or not script_text.strip():
            errors.append("Script text cannot be empty.")
            return False, errors

        words = script_text.strip().split()
        if len(words) < min_words:
            errors.append(f"Script word count ({len(words)}) is below minimum of {min_words} words.")

        return len(errors) == 0, errors

    @staticmethod
    def parse_segments(script_text: str) -> List[ScriptSegment]:
        """Parses script lines or dialogue tags into structured segments."""
        if not script_text:
            return []

        segments = []
        lines = script_text.strip().split("\n")
        
        for line in lines:
            trimmed = line.strip()
            if not trimmed:
                continue

            # Check timing tags e.g. [0:00], [01:30]
            timing_match = re.match(r"^\[(\d{1,2}:\d{2})\]\s*(.*)", trimmed)
            timing_tag = None
            text = trimmed

            if timing_match:
                timing_tag = timing_match.group(1)
                text = timing_match.group(2)

            # Check speaker tags e.g. "Host:", "Teacher:", "Student:"
            speaker_match = re.match(r"^(Host|Teacher|Student|Narrator|Alex|Sarah):\s*(.*)", text, re.IGNORECASE)
            speaker = "Host"
            if speaker_match:
                speaker = speaker_match.group(1).capitalize()
                text = speaker_match.group(2)

            emphasis = "[EMPHASIS]" in text or "[IMPORTANT]" in text
            clean_text = text.replace("[EMPHASIS]", "").replace("[IMPORTANT]", "").strip()

            segments.append(ScriptSegment(
                speaker=speaker,
                text=clean_text,
                timing_tag=timing_tag,
                emphasis=emphasis,
            ))

        return segments

    @staticmethod
    def extract_questions(script_text: str) -> List[str]:
        """Extracts interactive questions marked with ? or Q1: / Question: prefix."""
        if not script_text:
            return []

        questions = []
        lines = script_text.strip().split("\n")
        for line in lines:
            trimmed = line.strip()
            # Look for lines with question markers or ending with ?
            if re.match(r"^(Q\d+:|Question\s*\d*:|\d+\.)\s*.*\?", trimmed, re.IGNORECASE):
                questions.append(trimmed)
            elif "?" in trimmed and len(trimmed) < 200 and not trimmed.startswith("http"):
                # Clean prompt questions
                clean_q = re.sub(r"^\[.*?\]\s*", "", trimmed)
                clean_q = re.sub(r"^(Host|Teacher|Narrator):\s*", "", clean_q, flags=re.IGNORECASE)
                if clean_q.endswith("?"):
                    questions.append(clean_q)

        return list(dict.fromkeys(questions))[:10]  # Deduplicate and cap


class PodcastAccuracyPolicy:
    """Domain policy evaluating podcast readiness, duration correctness, and content validity."""

    @staticmethod
    def evaluate_accuracy(podcast: DailyPodcastEntity, target_min_sec: int = 300, target_max_sec: int = 420) -> Dict[str, Any]:
        issues = []
        warnings = []
        accuracy_score = 1.0

        # 1. Status verification
        if podcast.status == PodcastStatus.FAILED:
            issues.append("❌ Podcast generation failed")
            accuracy_score -= 0.5
        elif podcast.status == PodcastStatus.PENDING:
            return {
                "status": "pending",
                "message": "Podcast still generating. Please check again soon.",
                "accuracy_score": 0.0,
                "issues": [],
                "warnings": ["Podcast generation in progress"],
                "recommendation": "⏳ Pending generation",
            }

        # 2. Included courses check
        if not podcast.included_courses:
            warnings.append("⚠️ No courses mentioned in podcast")
            accuracy_score -= 0.1

        # 3. Audio status check
        audio_status = "❌ No audio"
        if podcast.output_format in [OutputFormat.AUDIO, OutputFormat.BOTH]:
            if podcast.audio_file_url:
                audio_status = "✅ Primary audio OK"
                if podcast.secondary_language and not podcast.audio_file_secondary_url:
                    warnings.append("⚠️ Secondary language audio missing")
                    accuracy_score -= 0.15
                elif podcast.secondary_language:
                    audio_status = "✅ Both languages OK"
            else:
                issues.append("❌ Audio file missing (required by output format)")
                accuracy_score -= 0.3
        elif podcast.output_format == OutputFormat.TEXT:
            audio_status = "✅ Text-only (audio not required)"

        # 4. Duration check
        duration_status = f"✅ {podcast.duration_seconds // 60}:{podcast.duration_seconds % 60:02d}"
        if podcast.duration_seconds < target_min_sec:
            warnings.append(f"⚠️ Podcast too short ({podcast.duration_seconds // 60} min, target ~6 min)")
            accuracy_score -= 0.05
        elif podcast.duration_seconds > target_max_sec:
            warnings.append(f"⚠️ Podcast too long ({podcast.duration_seconds // 60} min, target ~6 min)")
            accuracy_score -= 0.05

        # 5. Q&A check
        qa_status = f"✅ {len(podcast.questions_asked)} questions"
        if not podcast.questions_asked:
            warnings.append("⚠️ No questions generated for interactive podcast")
            accuracy_score -= 0.1

        # 6. Script text check
        if not podcast.script_text or len(podcast.script_text) < 100:
            issues.append("❌ Script too short or empty")
            accuracy_score -= 0.3

        clamped_score = max(0.0, min(1.0, accuracy_score))

        recommendation = (
            "✅ Ready for use" if clamped_score >= 0.8 and not issues
            else "⚠️ Review issues before publishing" if issues
            else "✓ Minor issues but usable"
        )

        return {
            "status": "success",
            "accuracy_score": round(clamped_score, 2),
            "issues": issues,
            "warnings": warnings,
            "content_checks": {
                "script_length": len(podcast.script_text) if podcast.script_text else 0,
                "courses_mentioned": len(podcast.included_courses),
                "audio_status": audio_status,
                "duration_status": duration_status,
                "qa_status": qa_status,
            },
            "recommendation": recommendation,
        }


class ProficiencyEvaluationPolicy:
    """Domain policy evaluating CEFR / English proficiency levels and timing estimates."""

    @staticmethod
    def estimate_duration_seconds(script_text: str, words_per_minute: int = 150) -> int:
        if not script_text:
            return 0
        words = len(script_text.split())
        return max(60, ceil(words / max(1, words_per_minute) * 60))

    @staticmethod
    def evaluate_cefr_level(stats: Dict[str, Any]) -> str:
        ability_score = stats.get("ability_score")
        if ability_score is None:
            return "B1"

        if ability_score >= 750:
            return "C2"
        elif ability_score >= 650:
            return "C1"
        elif ability_score >= 520:
            return "B2"
        elif ability_score >= 400:
            return "B1"
        elif ability_score >= 280:
            return "A2"
        return "A1"
