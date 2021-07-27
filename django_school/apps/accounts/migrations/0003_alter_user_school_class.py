# Generated by Django 3.2.5 on 2021-07-27 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='school_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='classes.class'),
        ),
    ]