# Generated by Django 5.0.7 on 2024-07-17 17:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_renter_list_of_games'),
    ]

    operations = [
        migrations.AddField(
            model_name='renter',
            name='event',
            field=models.ForeignKey(default=27, on_delete=django.db.models.deletion.CASCADE, to='core.event'),
            preserve_default=False,
        ),
    ]
