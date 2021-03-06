from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.views import View

from django_school.apps.common.utils import (
    AjaxRequiredMixin, GetObjectCacheMixin, RolesRequiredMixin, ajax_required,
    does_the_teacher_teach_the_subject_to_the_class, roles_required)
from django_school.apps.users.models import ROLES
from tests.utils import ClassesMixin, LessonsMixin, UsersMixin


class RolesRequiredMixinTestCase(UsersMixin, TestCase):
    class DummyView(RolesRequiredMixin(ROLES.TEACHER), View):
        def get(self, *args, **kwargs):
            return HttpResponse("OK")

    def test_dispatch_raises_404_if_user_have_no_required_role(self):
        teacher = self.create_teacher()
        student = self.create_student()
        request = RequestFactory().get("/test")
        view = self.DummyView.as_view()

        request.user = teacher
        view(request)

        request.user = student
        with self.assertRaises(PermissionDenied):
            view(request)

    def test_dispatch_does_not_raise_404_if_user_is_superuser(self):
        superuser = self.create_superuser()
        request = RequestFactory().get("/test")
        view = self.DummyView.as_view()

        request.user = superuser
        view(request)


class TeacherStatusRequiredTestCase(UsersMixin, TestCase):
    @staticmethod
    @roles_required(ROLES.TEACHER)
    def dummy_view(request):
        return HttpResponse("OK")

    def test_decorated_view_raises_404_if_user_have_no_required_role(self):
        teacher = self.create_teacher()
        student = self.create_student()
        request = RequestFactory().get("/test")

        request.user = teacher
        self.dummy_view(request)

        request.user = student
        with self.assertRaises(PermissionDenied):
            self.dummy_view(request)

    def test_decorated_view_does_not_raise_404_if_user_is_superuser(self):
        superuser = self.create_superuser()
        request = RequestFactory().get("/test")
        request.user = superuser

        self.dummy_view(request)


class DoesTheTeacherTeachTheSubjectToTheClassTestCase(
    UsersMixin, ClassesMixin, LessonsMixin, TestCase
):
    def setUp(self):
        self.teacher = self.create_teacher()
        self.school_class = self.create_class()
        self.subject = self.create_subject()

    def test_if_teacher_teaches(self):
        self.create_lesson(self.subject, self.teacher, self.school_class)

        result = does_the_teacher_teach_the_subject_to_the_class(
            self.teacher, self.subject, self.school_class
        )

        self.assertTrue(result)

    def test_if_teacher_does_not_teach(self):
        result = does_the_teacher_teach_the_subject_to_the_class(
            self.teacher, self.subject, self.school_class
        )

        self.assertFalse(result)


class GetObjectCacheMixinTestCase(TestCase):
    class DummyBaseView(View):
        get_object_calls_counter = 0

        def get_object(self, *args, **kwargs):
            self.__class__.get_object_calls_counter += 1
            return "Object"

        def get(self, *args, **kwargs):
            return HttpResponse("OK")

    class DummyView(GetObjectCacheMixin, DummyBaseView):
        def get(self, *args, **kwargs):
            for _ in range(5):
                self.get_object()

    def test_caches_object(self):
        request = RequestFactory().get("/test")
        view = self.DummyView.as_view()

        view(request)

        self.assertEqual(self.DummyView.get_object_calls_counter, 1)


class AjaxRequiredMixinTestCase(TestCase):
    class DummyView(AjaxRequiredMixin, View):
        def get(self, *args, **kwargs):
            return HttpResponse("OK")

        def post(self, *args, **kwargs):
            return HttpResponse("OK")

    def test_raises_PermissionDenied_if_request_not_ajax_and_method_not_allowed(self):
        request = RequestFactory().get("/test")
        view = self.DummyView.as_view()

        with self.assertRaises(PermissionDenied):
            view(request)

    def test_does_not_raise_if_request_is_ajax(self):
        request = RequestFactory().get("/test", HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        view = self.DummyView.as_view()

        view(request)

    def test_does_not_raise_if_request_method_in_not_ajax_but_in_allowed_methods(self):
        request = RequestFactory().post("/test")
        view = self.DummyView.as_view()

        view(request)

    def test_does_not_raise_if_request_is_htmx(self):
        request = RequestFactory().get("/test", HTTP_HX_REQUEST="true")
        view = self.DummyView.as_view()

        view(request)


class AjaxRequiredDecoratorTestCase(TestCase):
    @staticmethod
    @ajax_required
    def dummy_view(request):
        return HttpResponse("OK")

    def test_raises_PermissionDenied_if_request_not_ajax_and_method_not_allowed(self):
        request = RequestFactory().get("/test")

        with self.assertRaises(PermissionDenied):
            self.dummy_view(request)

    def test_does_not_raise_if_request_is_ajax(self):
        request = RequestFactory().get("/test", HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        self.dummy_view(request)

    def test_does_not_raise_if_request_method_in_not_ajax_but_in_allowed_methods(self):
        request = RequestFactory().post("/test")

        self.dummy_view(request)

    def test_does_not_raise_if_request_is_htmx(self):
        request = RequestFactory().get("/test", HTTP_HX_REQUEST="true")

        self.dummy_view(request)
