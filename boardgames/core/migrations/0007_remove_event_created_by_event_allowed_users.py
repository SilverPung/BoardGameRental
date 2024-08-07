# Generated by Django 5.0.7 on 2024-07-15 12:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20240715_1213'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='created_by',
        ),
        migrations.AddField(
            model_name='event',
            name='allowed_users',
            field=models.ManyToManyField(default=None, related_name='allowed_access', to=settings.AUTH_USER_MODEL),
        ),
    ]
