# Generated by Django 5.0.7 on 2024-07-18 13:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_game_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renter',
            name='event',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.event'),
        ),
    ]
