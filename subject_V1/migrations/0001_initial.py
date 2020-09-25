# Generated by Django 3.1 on 2020-09-24 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('faculty_V1', '0001_initial'),
        ('institute_V1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('short', models.CharField(max_length=10)),
                ('lect_per_week', models.PositiveIntegerField()),
                ('prac_per_week', models.PositiveIntegerField()),
                ('load_per_week', models.PositiveIntegerField(default=0)),
                ('color', models.CharField(max_length=7)),
                ('Semester_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='institute_V1.semester')),
            ],
            options={
                'verbose_name_plural': 'Subject Details',
            },
        ),
        migrations.CreateModel(
            name='Subject_event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(blank=True, null=True)),
                ('load_carried', models.PositiveIntegerField()),
                ('Faculty_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty_V1.faculty_details')),
                ('Subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subject_V1.subject_details')),
            ],
            options={
                'verbose_name_plural': 'Subject events',
            },
        ),
    ]