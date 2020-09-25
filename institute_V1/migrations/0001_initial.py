# Generated by Django 3.1 on 2020-09-24 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('short', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Branch',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('short', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Department',
            },
        ),
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('short', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Institute',
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('block', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('Department_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='institute_V1.department')),
            ],
            options={
                'verbose_name_plural': 'Shift',
            },
        ),
        migrations.CreateModel(
            name='Slots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('Shift_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='institute_V1.shift')),
            ],
            options={
                'verbose_name_plural': 'Slots',
            },
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short', models.CharField(max_length=20)),
                ('Branch_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='institute_V1.branch')),
            ],
            options={
                'verbose_name_plural': 'Semester',
            },
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('Semester_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='institute_V1.semester')),
                ('Shift_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='institute_V1.shift')),
            ],
            options={
                'verbose_name_plural': 'Division',
            },
        ),
        migrations.AddField(
            model_name='department',
            name='Institute_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='institute_V1.institute'),
        ),
        migrations.AddField(
            model_name='branch',
            name='Department_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='institute_V1.department'),
        ),
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('batch_for', models.CharField(choices=[('lect', 'Lecture'), ('prac', 'Practical')], max_length=4)),
                ('Division_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='institute_V1.division')),
            ],
            options={
                'verbose_name_plural': 'Batch',
            },
        ),
        migrations.CreateModel(
            name='Admin_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Institute_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institute_V1.institute')),
            ],
            options={
                'verbose_name_plural': 'Admin Details',
            },
        ),
    ]