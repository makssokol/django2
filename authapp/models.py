from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta


def expiration_datetime():
    return now() + timedelta(hours=48)


class ArtShopUser(AbstractUser):
    avatar = models.ImageField(upload_to="users_avatars", blank=True)
    age = models.PositiveIntegerField(verbose_name="age", default=18)
    gender = models.CharField(verbose_name="gender", max_length=1, blank=True)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=expiration_datetime)

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True
        

class ArtShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'

    GENDER_CHOICES = (
        (MALE, 'Man'),
        (FEMALE, 'Woman')
    )
    
    user = models.OneToOneField(ArtShopUser, on_delete=models.CASCADE, null=True)
    tagline = models.CharField(verbose_name='tags', max_length=128, 
                               blank=True)
    aboutMe = models.TextField(verbose_name='about me', max_length=512, 
                               blank=True)
    gender = models.CharField(verbose_name='sex', max_length=1, 
                              choices=GENDER_CHOICES, blank=True)
    