# Generated by Django 3.2.7 on 2022-02-21 08:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_auto_20220218_1317"),
        ("lessons", "0012_rename_hand_over_date_homeworkrealisation_submission_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homeworkrealisation",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="homeworks_realisations",
                to="users.user",
            ),
        ),
    ]
