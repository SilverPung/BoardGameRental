# Generated by Django 5.0.7 on 2024-07-15 12:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_event_created_by_event_allowed_users'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='allowed_users',
            field=models.ManyToManyField(default=None, null=True, related_name='allowed_access', to=settings.AUTH_USER_MODEL),
        ),
    ]
