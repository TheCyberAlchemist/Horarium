# Generated by Django 3.1 on 2020-11-23 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject_V1', '0002_auto_20201123_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject_details',
            name='lect_per_week',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
