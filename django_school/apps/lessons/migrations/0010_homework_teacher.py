# Generated by Django 3.2.7 on 2022-02-20 13:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_auto_20220218_1317"),
        ("lessons", "0009_alter_homework_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="homework",
            name="teacher",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
