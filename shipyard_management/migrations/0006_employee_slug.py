# Generated by Django 4.2.16 on 2024-11-05 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipyard_management', '0005_remove_employee_is_main'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='slug',
            field=models.SlugField(blank=True, default='', null=True),
        ),
    ]
