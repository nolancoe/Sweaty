from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from datetime import datetime

class Season(models.Model):
    gametype = models.CharField(max_length=15)

    def __str__(self):
        return str(self.gametype)




class user_profile(AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    gamertag = models.CharField(max_length=15, unique=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/")
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'gamertag']



    def __str__(self):
        return str(self.gamertag)

    def get_absolute_url(self):
        return reverse('home')

class Team(models.Model):
    teamname = models.CharField(max_length=30)
    gametype = models.ForeignKey(Season, on_delete=models.CASCADE, blank=True, null=True)
    captain = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='captain', on_delete=models.CASCADE)
    teammembers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teammembers', blank=True)

    def __str__(self):
        return str(self.teamname)

class Match(models.Model):
    gametype = models.ForeignKey(Season, on_delete=models.CASCADE, blank=True, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,  blank=True, null=True, on_delete=models.SET_NULL)
    datetime = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return str(self.gametype) + ' | ' + str(self.datetime)

    def get_absolute_url(self):
        return reverse('matches')


