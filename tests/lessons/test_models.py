from django.core.exceptions import ValidationError
from django.test import TestCase

from django_school.apps.lessons.models import Lesson, Presence
from tests.utils import ClassesMixin, LessonsMixin, UsersMixin


class TestSubjectModel(LessonsMixin, TestCase):
    def test_slugify_on_save_if_slug_not_given(self):
        subject = self.create_subject(name="Computer Science")

        self.assertEqual(subject.slug, "computer-science")

    def test_does_not_slugify_if_slug_given(self):
        subject = self.create_subject(name="Computer Science", slug="cs")

        self.assertEqual(subject.slug, "cs")


class TestLessonModel(UsersMixin, ClassesMixin, LessonsMixin, TestCase):
    def setUp(self):
        self.teacher = self.create_teacher()
        self.school_class = self.create_class()
        self.student = self.create_user(
            username="student", school_class=self.school_class
        )
        self.subject = self.create_subject()

    def test_clean_raises_ValidationError_when_the_teacher_already_have_lesson_in_given_time(
        self,
    ):
        lesson = self.create_lesson(self.subject, self.teacher, self.school_class)

        with self.assertRaises(ValidationError):
            Lesson(
                subject=self.subject,
                teacher=self.teacher,
                school_class=self.school_class,
                time=self.DEFAULT_TIME,
                weekday=self.DEFAULT_WEEKDAY,
            ).clean()

    def test_clean_raises_ValidationError_if_teacher_is_not_in_teachers_group(self):
        with self.assertRaises(ValidationError):
            Lesson(
                subject=self.subject,
                teacher=self.student,
                school_class=self.school_class,
                time=self.DEFAULT_TIME,
                weekday=self.DEFAULT_WEEKDAY,
            ).clean()


class TestPresenceModel(UsersMixin, ClassesMixin, LessonsMixin, TestCase):
    def test_clean_raises_ValidationError_if_student_is_not_in_lesson_session_class(
        self,
    ):
        teacher = self.create_teacher()
        school_class = self.create_class()
        student = self.create_user(username="student")
        subject = self.create_subject()
        lesson = self.create_lesson(subject, teacher, school_class)
        lesson_session = self.create_lesson_session(lesson)

        with self.assertRaises(ValidationError):
            Presence(student=student, lesson_session=lesson_session).clean()