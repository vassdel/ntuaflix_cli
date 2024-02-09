# Generated by Django 5.0.2 on 2024-02-09 11:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cli', '0004_movie_average_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Name',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameID', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('namePoster', models.URLField(blank=True, null=True)),
                ('birthYear', models.IntegerField(blank=True, null=True)),
                ('deathYear', models.IntegerField(blank=True, null=True)),
                ('profession', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=255)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cli.movie')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cli.name')),
            ],
        ),
        migrations.AddField(
            model_name='name',
            name='nameTitles',
            field=models.ManyToManyField(through='cli.Participation', to='cli.movie'),
        ),
    ]