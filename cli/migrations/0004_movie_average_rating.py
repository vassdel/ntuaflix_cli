# Generated by Django 5.0.2 on 2024-02-08 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cli', '0003_movie'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='average_rating',
            field=models.FloatField(default=0),
        ),
    ]
