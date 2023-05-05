import datetime

from django.db import models

# Create your models here.

class Musician(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
class Song(models.Model):
    url = models.CharField(max_length=256, primary_key=True)

    def __str__(self):
        return self.url


class User(models.Model):
    first_name = models.CharField(max_length=64, null=False, default="")
    last_name = models.CharField(max_length=64, null=False, default="")
    email = models.EmailField(max_length=128, null=False, primary_key=True)
    age = models.IntegerField(null=False, default=0)
    hometown = models.IntegerField(max_length=64, null=False, default=00000)
    dob = models.DateField(max_length=1028, null=False, default=datetime.date.today())
    recommended_songs = models.ManyToManyField(Song, max_length=2048)

class UserSave(models.Model):
    user = models.ForeignKey(User, null=False, primary_key=True, on_delete=models.CASCADE)
    IDs = models.ManyToManyField(Song, null=False)
