# Generated by Django 3.1 on 2020-08-26 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TableV1', '0011_auto_20200826_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='day',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')], max_length=10),
        ),
    ]
