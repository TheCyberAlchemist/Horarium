# Generated by Django 3.1 on 2020-10-07 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute_V1', '0009_auto_20201006_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='slots',
            name='is_break',
            field=models.BooleanField(default=False),
        ),
    ]