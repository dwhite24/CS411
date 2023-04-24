from django.db import models

# Create your models here.


class Genre(models.Model):
    text = models.CharField(max_length=128, null=False)
    id = models.IntegerField(primary_key=True)


class Movie(models.Model):
    name = models.CharField(max_length=256, null=False)
    mid = models.IntegerField(null=False, primary_key=True)
    genre = models.ManyToManyField(Genre, max_length=1028)


class Song(models.Model):
    name = models.CharField(max_length=256, null=False)
    id = models.CharField(max_length=16, primary_key=True)


class User(models.Model):
    first_name = models.CharField(max_length=64, null=False)
    last_name = models.CharField(max_length=64, null=False)
    email = models.EmailField(max_length=128, null=False, primary_key=True)
    username = models.CharField(max_length=64, null=False)
    age = models.IntegerField(null=True)
    hometown = models.CharField(max_length=64, null=True)
    dob = models.DateField(max_length=32, null=True)
    recommended_movies = models.ManyToManyField(Movie, max_length=2048)
    recommended_songs = models.ManyToManyField(Song, max_length=2048)

class UserSave(models.Model):
    user = models.CharField(max_length=64, null=False, primary_key=True)
    songs = models.TextField()
