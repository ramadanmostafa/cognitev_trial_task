from django.db import models
from django.contrib.auth.models import User

from . import COUNTRY_CODES, GENDERS


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    country_code = models.CharField(choices=COUNTRY_CODES)
    phone_number = models.CharField(max_length=11)
    gender = models.CharField(choices=GENDERS)
    birthdate = models.DateField()
    avatar = models.FileField(upload_to='')
    email = models.EmailField(null=True, blank=True, max_length=256)


class UserStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=256)
