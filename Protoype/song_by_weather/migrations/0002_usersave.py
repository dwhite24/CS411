# Generated by Django 3.2.7 on 2023-04-24 00:52

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('song_by_weather', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSave',
            fields=[
                ('user', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('songs', jsonfield.fields.JSONField(default=dict)),
            ],
        ),
    ]
