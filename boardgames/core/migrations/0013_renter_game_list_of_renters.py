# Generated by Django 5.0.7 on 2024-07-17 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_remove_game_bgg_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Renter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('barcode', models.CharField(max_length=20)),
                ('list_of_games', models.ManyToManyField(related_name='rented_games', to='core.game')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='list_of_renters',
            field=models.ManyToManyField(related_name='rented_games', to='core.renter'),
        ),
    ]
