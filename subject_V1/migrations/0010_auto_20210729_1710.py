# Generated by Django 3.2.3 on 2021-07-29 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject_V1', '0009_rename_co_faculty_id_subject_event_co_faculty_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject_event',
            old_name='Co_Faculty_id',
            new_name='Co_faculty_id',
        ),
        migrations.AddConstraint(
            model_name='subject_event',
            constraint=models.UniqueConstraint(fields=('Faculty_id', 'Co_faculty_id'), name='Co-faculty and Faculty need to be Unique.'),
        ),
        migrations.AddConstraint(
            model_name='subject_event',
            constraint=models.UniqueConstraint(fields=('Co_faculty_id', 'Subject_id'), name='Subject can have only one Unique Co-faculty.'),
        ),
    ]