# Generated by Django 4.2.16 on 2024-11-05 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipyard_management', '0003_remove_employee_is_main_alter_employee_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='is_main',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='employee',
            name='status',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='project',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(max_length=50),
        ),
    ]
