# Generated by Django 3.1 on 2020-11-23 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute_V1', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='division',
            name='DivisionName is Unique for Semester',
        ),
        migrations.RemoveConstraint(
            model_name='semester',
            name='SemesterShort is Unique for Branch',
        ),
        migrations.RemoveConstraint(
            model_name='shift',
            name='ShiftName is Unique for Institute',
        ),
        migrations.AddConstraint(
            model_name='division',
            constraint=models.UniqueConstraint(fields=('name', 'Semester_id'), name='Division Name is Unique for Semester'),
        ),
        migrations.AddConstraint(
            model_name='semester',
            constraint=models.UniqueConstraint(fields=('short', 'Branch_id'), name='Semester Short is Unique for Branch'),
        ),
        migrations.AddConstraint(
            model_name='shift',
            constraint=models.UniqueConstraint(fields=('name', 'Department_id'), name='ShiftName is Unique for Department'),
        ),
    ]
