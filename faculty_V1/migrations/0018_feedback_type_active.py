# Generated by Django 3.2.3 on 2021-05-26 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faculty_V1', '0017_auto_20210526_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback_type',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
