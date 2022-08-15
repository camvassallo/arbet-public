# Generated by Django 3.2.12 on 2022-05-26 03:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sportsbook', '0006_alter_bet_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bet',
            name='game_id',
        ),
        migrations.AddField(
            model_name='bet',
            name='game',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sportsbook.game'),
        ),
    ]