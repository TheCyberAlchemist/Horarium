# Generated by Django 3.2.3 on 2021-07-31 03:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student_V1', '0006_rename_user_id_student_logs_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student_logs',
            old_name='User_id',
            new_name='user_id',
        ),
    ]