# Generated by Django 3.1 on 2020-12-17 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute_V1', '0005_auto_20201212_0115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='block',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='resource',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]