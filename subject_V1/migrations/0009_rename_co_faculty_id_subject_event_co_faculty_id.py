# Generated by Django 3.2.3 on 2021-07-22 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subject_V1', '0008_auto_20210722_0000'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject_event',
            old_name='Co_faculty_id',
            new_name='Co_Faculty_id',
        ),
    ]
