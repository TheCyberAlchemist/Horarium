# Generated by Django 3.1 on 2021-03-25 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institute_V1', '0012_wef'),
    ]

    operations = [
        migrations.AddField(
            model_name='semester',
            name='WEF_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='institute_V1.wef'),
        ),
    ]