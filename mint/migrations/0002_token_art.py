# Generated by Django 3.2.12 on 2022-07-19 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mint', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='art',
            field=models.ImageField(blank=True, upload_to='token_art'),
        ),
    ]
