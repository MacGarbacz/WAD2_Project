from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify



class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User,related_name="profile_user")

    # The additional attributes we wish to include.
    picture = models.ImageField(upload_to='profile_images', blank=True)
    
    list = models.ManyToManyField('Character', through='ListElement', through_fields=('user', 'character'))


    # Override the __unicode__() method to return out something meaningful!
    def __str__(self):
        return self.user.username

class VideoGame(models.Model):
    name = models.CharField(max_length=128, help_text='Please Enter the videogame title' ,unique =True)
    slug = models.SlugField()
    picture = models.ImageField(upload_to='game_images', help_text='Add Video Game Picture', blank=True)

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
    name = models.CharField(max_length=128,
                            help_text='Please enter the name of the character.')
    slug = models.SlugField()
    url = models.URLField(max_length=200,blank=True,
                         help_text='Please enter the URL of the character.')
    bio = models.CharField(max_length=512,
                            help_text='Please enter the bio of the character.')

    picture = models.ImageField(upload_to='char_images', help_text='Add Character Picture', blank=True)
    ratings = models.ManyToManyField(UserProfile, through='Rating', through_fields=('character', 'user'), default = 0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Character, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Character'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Rating(models.Model):
    user = models.ForeignKey(UserProfile)
    character = models.ForeignKey(Character)
    rating = models.IntegerField(default = 0,choices=[(i,i) for i in range(101)])
    class Meta:
        #user cannot rate a character twice
        unique_together = ('user', 'character')

    def __str__(self):
        return str(self.rating)

    def __unicode__(self):
        return str(self.rating)


class ListElement(models.Model):
    user = models.ForeignKey(UserProfile)
    character = models.ForeignKey(Character ,blank = True)
    position = models.IntegerField(choices=[(i,i) for i in range(11)])
    class Meta:
        #same list position cannot appear twice in a list, same character cannot appear twice in a list
        unique_together = (('user', 'position'), ('user', 'character'))
    def __str__(self):
        return self.user.user.username + " " + self.character.name + " " + str(self.position)

    def __unicode__(self):
        return self.user.user.username + " " + self.character.name + " " + str(self.position)