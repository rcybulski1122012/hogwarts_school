# Generated by Django 3.2.6 on 2021-08-22 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0004_class_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
