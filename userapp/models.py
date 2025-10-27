from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True)
    profile_image = models.ImageField(null=True, blank=True)

class Banners(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True,upload_to='banners/')