# Generated by Django 3.2.3 on 2021-07-31 01:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institute_V1', '0022_alter_semester_wef_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student_V1', '0004_auto_20210529_1549'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student_logs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=64)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('ip', models.GenericIPAddressField(null=True)),
                ('Division_id', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institute_V1.division')),
                ('user_id', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
