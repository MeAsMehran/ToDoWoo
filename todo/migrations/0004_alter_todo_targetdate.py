# Generated by Django 5.1 on 2024-08-27 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_alter_todo_createddate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='targetDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
