from django.db import models
from django.contrib.auth.models import AbstractUser

class ArtShopUser(AbstractUser):
    avatar = models.ImageField(upload_to="users_avatars", blank=True)
    age = models.PositiveIntegerField(verbose_name="age")
    gender = models.CharField(verbose_name="gender", max_length=1)
