# Generated by Django 3.2.12 on 2022-07-18 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsbook', '0011_game_last_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='ml_win_art',
            field=models.ImageField(blank=True, upload_to='ml_win_art'),
        ),
        migrations.AddField(
            model_name='game',
            name='spread_win_art',
            field=models.ImageField(blank=True, upload_to='spread_win_art'),
        ),
    ]
