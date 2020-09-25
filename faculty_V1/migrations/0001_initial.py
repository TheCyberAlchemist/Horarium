# Generated by Django 3.1 on 2020-09-24 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Can_teach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'Can teach',
            },
        ),
        migrations.CreateModel(
            name='Faculty_designation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Faculty Designation',
            },
        ),
        migrations.CreateModel(
            name='Faculty_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short', models.CharField(max_length=10)),
                ('Designation_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='faculty_V1.faculty_designation')),
            ],
            options={
                'verbose_name_plural': 'Faculty Details',
            },
        ),
        migrations.CreateModel(
            name='Faculty_load',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('load', models.IntegerField()),
                ('Faculty_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty_V1.faculty_details')),
            ],
            options={
                'verbose_name_plural': 'Faculty load',
            },
        ),
    ]
