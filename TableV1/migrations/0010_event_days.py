# Generated by Django 3.1 on 2020-08-26 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TableV1', '0009_timings_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='days',
            field=models.CharField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], default=0, max_length=1),
            preserve_default=False,
        ),
    ]