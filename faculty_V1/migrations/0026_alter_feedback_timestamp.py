# Generated by Django 3.2.3 on 2021-08-28 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faculty_V1', '0025_faculty_details_resource_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
