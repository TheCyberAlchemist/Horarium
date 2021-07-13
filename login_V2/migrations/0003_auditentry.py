# Generated by Django 3.2.3 on 2021-07-13 09:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_V2', '0002_auto_20210525_1530'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=64)),
                ('forwarded_ip', models.TextField(null=True)),
                ('ip', models.GenericIPAddressField(null=True)),
                ('email_used', models.CharField(max_length=256, null=True)),
                ('password_used', models.TextField(null=True)),
                ('user_agent', models.TextField(null=True)),
                ('user_id', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]