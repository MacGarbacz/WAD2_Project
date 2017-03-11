from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify



class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User,related_name="profile_user")

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    # Remember if you use Python 2.7.x, define __unicode__ too!
    def __str__(self):
        return self.user.username

class VideoGame(models.Model):
    name = models.CharField(max_length=128, unique =True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(VideoGame, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'VideoGames'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Character(models.Model):
    videogame = models.ForeignKey(VideoGame)
    name = models.CharField(max_length=128)
    url = models.URLField()
    bio = models.CharField(max_length=512)


    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
