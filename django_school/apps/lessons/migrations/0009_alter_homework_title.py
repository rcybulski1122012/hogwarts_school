# Generated by Django 3.2.7 on 2022-02-19 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lessons", "0008_delete_attachedfile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homework",
            name="title",
            field=models.CharField(max_length=64),
        ),
    ]
