# Generated by Django 3.1 on 2021-02-03 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faculty_V1', '0005_auto_20201128_2000'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=220)),
                ('money', models.IntegerField()),
            ],
        ),
    ]