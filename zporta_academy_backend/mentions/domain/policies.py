import re
from typing import List


class MentionParserPolicy:
    """Pure domain logic for parsing @mentions in post/comment/text bodies."""

    @staticmethod
    def extract_usernames(text: str) -> List[str]:
        if not text:
            return []
        # Match @username pattern (alphanumeric, underscores)
        matches = re.findall(r'@([a-zA-Z0-9_]+)', text)
        # Deduplicate while preserving order
        seen = set()
        result = []
        for m in matches:
            if m not in seen:
                seen.add(m)
                result.append(m)
        return result
