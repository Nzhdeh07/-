from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator


class Song(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='songs')
    title = models.CharField(max_length=20)
    audio_file = models.FileField(upload_to='audio/', validators=[FileExtensionValidator(['mp3', 'wav'])])
    image = models.ImageField(upload_to='images/', validators=[FileExtensionValidator(['jpg', 'png'])])

    def __str__(self):
        return self.title

@receiver(post_delete, sender=Song)
def delete_song_files(sender, instance, **kwargs):
    instance.audio_file.delete(False)
    instance.image.delete(False)


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    title = models.CharField(max_length=20)
    songs = models.ManyToManyField('Song', related_name='playlists')
    image = models.ImageField(upload_to='images/', validators=[FileExtensionValidator(['jpg', 'png'])])

    def __str__(self):
        return self.title

@receiver(post_delete, sender=Playlist)
def delete_song_files(sender, instance, **kwargs):
    instance.image.delete(False)
