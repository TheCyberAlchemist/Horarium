# Generated by Django 3.2.3 on 2021-05-29 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subject_V1', '0006_remove_subject_event_link'),
        ('faculty_V1', '0020_alter_feedback_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='Subject_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='subject_V1.subject_details'),
        ),
    ]