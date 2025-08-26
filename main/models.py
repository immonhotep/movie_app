from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from django.utils import timezone
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from tinymce.models import HTMLField

from urllib.request import urlopen
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.validators import FileExtensionValidator
from django.db.models import Avg,Count




class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = ResizedImageField(size=[800, 600], upload_to='images/profiles',null=True)
    

    def __str__(self):
        return self.user.username

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
@receiver(post_save, sender=User)
def handler_function(sender, instance, created, **kwargs):
    if  created:
        profile = Profile(user=instance)
        profile.save()


class Watchlist(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tmdb_id = models.PositiveIntegerField(null=True, blank=True)
    title = models.CharField(max_length=255,null=True, blank=True)
    poster_url = models.URLField(null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return str(self.title)



class MovieReview(models.Model):

    body = HTMLField(null=False,max_length=3000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_tmdb_id = models.PositiveIntegerField(null=True,blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    poster_url = models.URLField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated =  models.DateTimeField(auto_now=True)
    allowed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)


class MovieRating(models.Model):

    rate = models.PositiveIntegerField(default=0)
    movie_tmdb_id = models.PositiveIntegerField(null=True,blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    poster_url = models.URLField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated =  models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.movie_tmdb_id)
    


class PersonReview(models.Model):

    body = HTMLField(null=False,max_length=3000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    person_tmdb_id = models.PositiveIntegerField(null=True,blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    poster_url = models.URLField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated =  models.DateTimeField(auto_now=True)
    allowed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class PersonRating(models.Model):

    rate = models.PositiveIntegerField(default=0)
    person_tmdb_id = models.PositiveIntegerField(null=True,blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    poster_url = models.URLField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated =  models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.person_tmdb_id)

    








