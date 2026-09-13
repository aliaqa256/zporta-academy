"""
Standard test data factories for characterization test suites.
Creates deterministic test records for Users, Courses, Lessons, Quizzes, and Intelligence models.
"""
from django.contrib.auth.models import User
from users.models import Profile
from courses.models import Course
from subjects.models import Subject
from lessons.models import Lesson
from quizzes.models import Quiz, Question


def create_test_user(username: str = "test_student", email: str = "student@test.com", password: str = "P@ssword123!", role: str = "explorer") -> User:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={"email": email}
    )
    if created:
        user.set_password(password)
        user.save()
    profile, _ = Profile.objects.get_or_create(user=user, defaults={"role": role, "display_name": username.title()})
    return user


def create_test_teacher(username: str = "test_teacher", email: str = "teacher@test.com", password: str = "P@ssword123!") -> User:
    user, created = User.objects.get_or_create(
        username=username,
        defaults={"email": email}
    )
    if created:
        user.set_password(password)
        user.save()
    Profile.objects.get_or_create(
        user=user,
        defaults={"role": "guide", "active_guide": True, "display_name": "Sensei Test"}
    )
    return user


def create_test_subject(author: User, name: str = "Japanese") -> Subject:
    subject, _ = Subject.objects.get_or_create(
        name=name,
        defaults={"created_by": author}
    )
    return subject


def create_test_course(author: User, title: str = "Beginner Japanese", permalink: str = "beginner-japanese") -> Course:
    subject = create_test_subject(author)
    course, _ = Course.objects.get_or_create(
        permalink=permalink,
        defaults={
            "title": title,
            "description": "Learn basic Japanese hiragana and grammar.",
            "created_by": author,
            "subject": subject,
            "is_draft": False,
            "course_type": "free",
        }
    )
    return course


def create_test_lesson(author: User, course: Course, title: str = "Lesson 1: Greetings", permalink: str = "lesson-1-greetings") -> Lesson:
    subject = create_test_subject(author)
    lesson, _ = Lesson.objects.get_or_create(
        permalink=permalink,
        defaults={
            "title": title,
            "content": "<p>Welcome to Lesson 1: Konnichiwa!</p>",
            "created_by": author,
            "subject": subject,
            "course": course,
            "status": "published",
        }
    )
    return lesson


def create_test_quiz(author: User, title: str = "Japanese Basics Quiz", permalink: str = "japanese-basics-quiz") -> Quiz:
    subject = create_test_subject(author)
    quiz, _ = Quiz.objects.get_or_create(
        permalink=permalink,
        defaults={
            "title": title,
            "content": "Test your Japanese basics knowledge.",
            "created_by": author,
            "subject": subject,
            "status": "published",
        }
    )
    if not quiz.questions.exists():
        Question.objects.create(
            quiz=quiz,
            question_text="What does 'Konnichiwa' mean?",
            question_type="mcq",
            option1="Hello / Good day",
            option2="Good bye",
            option3="Thank you",
            option4="Excuse me",
            correct_option=1
        )
    return quiz
