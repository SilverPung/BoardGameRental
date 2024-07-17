# Generated by Django 5.0.7 on 2024-07-17 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_renter_game_list_of_renters'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renter',
            name='list_of_games',
            field=models.ManyToManyField(blank=True, default=None, related_name='rented_games', to='core.game'),
        ),
    ]
