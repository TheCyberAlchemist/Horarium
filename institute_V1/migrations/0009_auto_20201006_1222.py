# Generated by Django 3.1 on 2020-10-06 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute_V1', '0008_auto_20201006_1216'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='batch',
            constraint=models.UniqueConstraint(fields=('name', 'Division_id'), name='BatchName is Unique for Division'),
        ),
        migrations.AddConstraint(
            model_name='branch',
            constraint=models.UniqueConstraint(fields=('short', 'Department_id'), name='BranchShort is Unique for Department'),
        ),
        migrations.AddConstraint(
            model_name='division',
            constraint=models.UniqueConstraint(fields=('name', 'Semester_id'), name='DivisionName is Unique for Semester'),
        ),
        migrations.AddConstraint(
            model_name='semester',
            constraint=models.UniqueConstraint(fields=('short', 'Branch_id'), name='SemesterShort is Unique for Branch'),
        ),
        migrations.AddConstraint(
            model_name='slots',
            constraint=models.UniqueConstraint(fields=('name', 'Shift_id'), name='SlotName is Unique for Shift'),
        ),
    ]