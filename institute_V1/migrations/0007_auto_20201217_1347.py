# Generated by Django 3.1 on 2020-12-17 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute_V1', '0006_auto_20201217_1340'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resource',
            options={'verbose_name_plural': 'Resource'},
        ),
        migrations.AddConstraint(
            model_name='resource',
            constraint=models.UniqueConstraint(fields=('name', 'Institute_id'), name='Resource Name is Unique for Institute'),
        ),
    ]
