# Generated by Django 4.2 on 2023-04-20 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('text', models.CharField(max_length=128)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('name', models.CharField(max_length=256)),
                ('mid', models.IntegerField(primary_key=True, serialize=False)),
                ('genre', models.ManyToManyField(max_length=1028, to='song_by_weather.genre')),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('name', models.CharField(max_length=256)),
                ('id', models.CharField(max_length=16, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=128, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=64)),
                ('age', models.IntegerField(null=True)),
                ('hometown', models.CharField(max_length=64, null=True)),
                ('dob', models.DateField(max_length=32, null=True)),
                ('recommended_movies', models.ManyToManyField(max_length=2048, to='song_by_weather.movie')),
                ('recommended_songs', models.ManyToManyField(max_length=2048, to='song_by_weather.song')),
            ],
        ),
    ]
