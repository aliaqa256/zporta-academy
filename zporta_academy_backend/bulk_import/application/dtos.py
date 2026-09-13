from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class ImportValidationDTO:
    is_valid: bool
    errors: List[Dict[str, str]] = field(default_factory=list)
    warnings: List[Dict[str, str]] = field(default_factory=list)
    total_courses: int = 0
    total_lessons: int = 0
    total_quizzes: int = 0
    total_questions: int = 0


@dataclass
class ImportResultDTO:
    success: bool
    message: str
    job_id: str
    total_courses: int = 0
    total_lessons: int = 0
    total_quizzes: int = 0
    total_questions: int = 0
    errors: List[str] = field(default_factory=list)
