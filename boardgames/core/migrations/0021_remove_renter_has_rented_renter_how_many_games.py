# Generated by Django 5.0.7 on 2024-07-18 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_renter_has_rented'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='renter',
            name='has_rented',
        ),
        migrations.AddField(
            model_name='renter',
            name='how_many_games',
            field=models.IntegerField(default=0),
        ),
    ]
