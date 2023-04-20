from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from extentions.utils import jalali_converter


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f'{instance.username}{ext}'
    return f'profile/{instance.username}/{final_name}'


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    image = models.ImageField(null=True, blank=True, upload_to=upload_image_path)
    job = models.CharField(null=True, blank=True, max_length=50, verbose_name='شغل')
    bio = models.CharField(null=True, blank=True, max_length=200, verbose_name='بیوگرافی')
    linkedin = models.CharField(null=True, blank=True, max_length=200, verbose_name='لینکدین')
    instagram = models.CharField(null=True, blank=True, max_length=200, verbose_name='اینستاگرام')
    twitter = models.CharField(null=True, blank=True, max_length=200, verbose_name='توئیتر')
    githb = models.CharField(null=True, blank=True, max_length=200, verbose_name='گیت هاب')
    telegram = models.CharField(null=True, blank=True, max_length=200, verbose_name='تلگرام')

    @property
    def get_date_join(self):
        return jalali_converter(self.date_joined)

    @property
    def get_last_login(self):
        return jalali_converter(self.last_login.date())
