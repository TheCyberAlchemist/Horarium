# Generated by Django 3.2.3 on 2021-08-23 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institute_V1', '0022_alter_semester_wef_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='division',
            name='Resource_id',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institute_V1.resource'),
        ),
        migrations.AddField(
            model_name='resource',
            name='is_lab',
            field=models.BooleanField(default=False),
        ),
    ]