# Generated by Django 3.2.3 on 2021-05-30 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faculty_V1', '0021_feedback_subject_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback_type',
            name='active',
            field=models.IntegerField(),
        ),
    ]