# Generated by Django 3.2.6 on 2021-08-21 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='slug',
            field=models.SlugField(default='o', max_length=64, unique=True),
            preserve_default=False,
        ),
    ]
