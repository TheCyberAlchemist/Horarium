# Generated by Django 3.1 on 2020-10-06 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute_V1', '0006_resource_institute_id'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='department',
            constraint=models.UniqueConstraint(fields=('short', 'Institute_id'), name='Short is Unique for Institute'),
        ),
    ]