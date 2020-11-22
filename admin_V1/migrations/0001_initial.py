# Generated by Django 3.1 on 2020-11-22 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institute_V1', '0001_initial'),
        ('login_V2', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin_details',
            fields=[
                ('User_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='login_V2.customuser')),
                ('Institute_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institute_V1.institute')),
            ],
            options={
                'verbose_name_plural': 'Admin Details',
            },
        ),
    ]
