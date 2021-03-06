from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class ClassQuerySet(models.QuerySet):
    def with_students(self):
        return self.select_related("tutor").prefetch_related("students")

    def visible_to_user(self, user):
        if user.is_teacher:
            return self.filter(lessons__teacher=user).distinct()
        elif user.is_student:
            return self.filter(pk=user.school_class_id)
        elif user.is_parent:
            return self.filter(pk=user.child.school_class_id)


class Class(models.Model):
    number = models.CharField(max_length=32, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    tutor = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        null=True,
        related_name="teacher_class",
    )

    objects = ClassQuerySet.as_manager()

    class Meta:
        verbose_name_plural = "classes"

    def __str__(self):
        return self.number

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.number)
        super().save(**kwargs)

    def clean(self):
        super().clean()

        if self.tutor is not None and not self.tutor.is_teacher:
            raise ValidationError("Tutor is not a teacher.")

    @property
    def detail_url(self):
        return reverse("classes:detail", args=[self.slug])

    @property
    def timetable_url(self):
        return reverse("lessons:class_timetable", args=[self.slug])

    @property
    def attendance_url(self):
        return reverse("lessons:class_attendance", args=[self.slug])

    @property
    def subject_list_url(self):
        return reverse("lessons:class_subject_list", args=[self.slug])

    @property
    def summary_pdf_url(self):
        return reverse("classes:summary_pdf", args=[self.slug])
