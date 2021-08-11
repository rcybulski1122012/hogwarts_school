from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django_school.apps.users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                "fields": (
                    "personal_id",
                    "phone_number",
                    "gender",
                    "address",
                    "school_class",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "personal_id",
                    "phone_number",
                    "gender",
                    "address",
                    "school_class",
                )
            },
        ),
    )
