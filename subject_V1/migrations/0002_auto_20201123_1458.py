# Generated by Django 3.1 on 2020-11-23 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject_V1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject_details',
            name='prac_per_week',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]