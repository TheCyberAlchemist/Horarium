# Generated by Django 3.1 on 2021-02-07 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        # ('institute_V1', '0008_auto_20210105_1724'),
        ('admin_V1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin_details',
            name='Institute_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='institute_V1.institute'),
            preserve_default=False,
        ),
    ]
