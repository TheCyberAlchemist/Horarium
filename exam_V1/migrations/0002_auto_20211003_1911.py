# Generated by Django 3.1 on 2021-10-03 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam_V1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='subject_exam',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]