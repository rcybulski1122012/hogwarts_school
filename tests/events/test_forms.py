import datetime

from django.test import TestCase

from django_school.apps.classes.models import Class
from django_school.apps.events.forms import EventForm
from django_school.apps.events.models import EventStatus
from tests.utils import ClassesMixin, EventsMixin, LessonsMixin, UsersMixin


class EventFormTestCase(UsersMixin, ClassesMixin, LessonsMixin, EventsMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.teacher = cls.create_teacher()
        cls.school_class = cls.create_class()
        cls.student = cls.create_student(school_class=cls.school_class)
        cls.date = datetime.date.today() + datetime.timedelta(days=1)
        cls.event = cls.create_event(cls.teacher, cls.school_class, cls.date)

    def test_class_queryset(self):
        subject = self.create_subject()
        teacher2 = self.create_teacher(username="teacher2")
        school_class2 = self.create_class(number="2c")
        self.create_lesson(subject, self.teacher, self.school_class)
        self.create_lesson(subject, teacher2, school_class2)

        form = EventForm(user=teacher2)

        self.assertQuerysetEqual(
            form.fields["school_class"].queryset,
            Class.objects.visible_to_user(teacher2),
        )

    def test_is_valid_assigns_teacher_to_instance(self):
        form = EventForm(
            user=self.teacher,
        )

        form.is_valid()

        self.assertEqual(form.instance.teacher, self.teacher)

    def test_save_creates_event_statuses_if_commit_is_True(self):
        data = {
            "title": "Title",
            "date": self.date,
        }
        form = EventForm(user=self.teacher, data=data)

        form.is_valid()
        form.save()

        self.assertTrue(EventStatus.objects.exists())
