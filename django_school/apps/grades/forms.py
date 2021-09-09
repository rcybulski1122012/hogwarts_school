from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from django_school.apps.grades.models import Grade, GradeCategory
from django_school.apps.lessons.models import Subject

User = get_user_model()


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = [
            "grade",
            "category",
            "weight",
            "comment",
            "student",
            "subject",
            "teacher",
        ]
        widgets = {
            "subject": forms.HiddenInput(),
            "teacher": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        school_class = kwargs.pop("school_class")
        subject = kwargs.pop("subject")
        super().__init__(*args, **kwargs)

        self.fields["student"].queryset = User.objects.filter(school_class=school_class)
        self.fields["category"].queryset = GradeCategory.objects.filter(
            subject=subject, school_class=school_class
        )


class BulkGradeCreationCommonInfoForm(forms.Form):
    category = forms.ModelChoiceField(queryset=None)
    weight = forms.IntegerField(
        validators=[MinValueValidator(1, "Weight must be a positive number.")],
        required=True,
    )
    comment = forms.CharField(required=False, widget=forms.Textarea())
    teacher = forms.ModelChoiceField(
        queryset=User.objects.all(), widget=forms.HiddenInput()
    )
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(), widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        school_class = kwargs.pop("school_class")
        subject = kwargs.pop("subject")
        teacher = kwargs.pop("teacher")
        super().__init__(*args, **kwargs)

        self.fields["category"].queryset = GradeCategory.objects.filter(
            subject=subject, school_class=school_class
        )
        self.fields["teacher"].initial = teacher.pk
        self.fields["subject"].initial = subject.pk


class BulkGradeCreationForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = "__all__"
        widgets = {
            "student": forms.HiddenInput(),
            "weight": forms.HiddenInput(),
            "comment": forms.HiddenInput(),
            "category": forms.HiddenInput(),
            "subject": forms.HiddenInput(),
            "teacher": forms.HiddenInput(),
        }


class BaseBulkGradeCreationFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        self.students = kwargs.pop("students")
        super().__init__(*args, **kwargs)
        self.queryset = self.model.objects.none()

    def total_form_count(self):
        return len(self.students)

    def _construct_form(self, i, **kwargs):
        form = super()._construct_form(i, **kwargs)
        form.fields["student"].initial = self.students[i].pk
        form.student_label = self.students[i].full_name

        return form

    def set_common_data(self, common_data):
        data = self.data.copy()
        for i in range(self.total_form_count()):
            for key, value in common_data.items():
                data[f"form-{i}-{key}"] = value

        self.data = data


BulkGradeCreationFormSet = forms.modelformset_factory(
    Grade,
    form=BulkGradeCreationForm,
    labels={"grade": ""},
    formset=BaseBulkGradeCreationFormSet,
)
