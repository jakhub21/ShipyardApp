# Generated by Django 4.2.16 on 2024-11-07 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipyard_management', '0009_rename_emplotees_project_employees'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='projects',
            new_name='project',
        ),
        migrations.RemoveField(
            model_name='project',
            name='employees',
        ),
    ]
