from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=64, null=False)
    last_name = models.CharField(max_length=64, null=False)
    email = models.EmailField(max_length=128, null=False, primary_key=True)
    username = models.CharField(max_length=64, null=False)
    age = models.IntegerField(max_length=8, null=True)
    hometown = models.CharField(max_length=64, null=True)
    dob = models.DateField(max_length=32, null=True)


class Movie(models.Model):
    name = models.CharField(max_length=256, null=False)
    mid = models.IntegerField(max_length=16, null=False, primary_key=True)
    MOVIE_GENRE_CHOICES = [
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('GR', 'Graduate'),
    ]
    genre = models.CharField(models.TextChoices, max_length=50)

