from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class ValidationIssue:
    level: str  # "error" or "warning"
    path: str
    message: str


@dataclass
class ValidationReportEntity:
    is_valid: bool
    errors: List[ValidationIssue] = field(default_factory=list)
    warnings: List[ValidationIssue] = field(default_factory=list)
    total_courses: int = 0
    total_lessons: int = 0
    total_quizzes: int = 0
    total_questions: int = 0


@dataclass
class BulkImportJobEntity:
    id: str
    created_by_id: int
    status: str
    total_courses: int = 0
    total_lessons: int = 0
    total_quizzes: int = 0
    total_questions: int = 0
    processed_courses: int = 0
    processed_lessons: int = 0
    processed_quizzes: int = 0
    processed_questions: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    summary: str = ""
