# Generated by Django 3.1 on 2020-08-26 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TableV1', '0007_timings_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timings',
            name='owner',
        ),
    ]
