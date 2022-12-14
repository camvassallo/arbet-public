# Generated by Django 3.2.12 on 2022-07-19 03:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sportsbook', '0012_auto_20220717_2002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.FloatField(default=0.0)),
                ('mint_status', models.CharField(default='PENDING', max_length=20)),
                ('bet', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sportsbook.bet')),
            ],
        ),
    ]
