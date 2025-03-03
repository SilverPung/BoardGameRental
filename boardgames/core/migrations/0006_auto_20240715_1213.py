# Generated by Django 5.0.7 on 2024-07-15 12:13

from django.db import migrations
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

def create_users(apps, schema_editor):
    User = get_user_model()
    # Create a superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@admin.com', 'mysiopysio123')
    
    # Create a moderator user
    if not User.objects.filter(username='moderator').exists():
        User.objects.create_user('moderator', 'moderator@example.com', 'mysiopysio')
       

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_event_created_by'),
    ]

    operations = [
        migrations.RunPython(create_users)
    ]
