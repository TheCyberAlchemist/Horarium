# Generated by Django 3.2.3 on 2021-09-18 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student_V1', '0008_sticky_notes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student_logs',
            options={'verbose_name_plural': 'Student Logs'},
        ),
        migrations.AlterModelOptions(
            name='user_notes',
            options={'verbose_name_plural': 'User Notes'},
        ),
    ]
