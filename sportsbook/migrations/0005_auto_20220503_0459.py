# Generated by Django 3.2.12 on 2022-05-03 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportsbook', '0004_bet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bet',
            name='bet_payout',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='bet',
            name='bet_value',
            field=models.FloatField(default=0.0),
        ),
    ]
