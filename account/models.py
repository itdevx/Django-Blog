from re import T
from django.db import models
from django.contrib.auth.models import AbstractUser
import os


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f'{instance.username}{ext}'
    return f'profile/{instance.username}/{final_name}'


class User(AbstractUser):
    email = models.EmailField(unique=True)
    image = models.ImageField(null=True, blank=True, upload_to=upload_image_path)
    job = models.CharField(null=True, blank=True, max_length=50)
    bio = models.CharField(null=True, blank=True, max_length=200)
    linkedin = models.CharField(null=True, blank=True, max_length=200)
    instagram = models.CharField(null=True, blank=True, max_length=200)
    twitter = models.CharField(null=True, blank=True, max_length=200)
    githb = models.CharField(null=True, blank=True, max_length=200)
    telegram = models.CharField(null=True, blank=True, max_length=200)