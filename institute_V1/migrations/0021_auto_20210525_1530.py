# Generated by Django 3.1 on 2021-05-25 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute_V1', '0020_auto_20210525_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wef',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
