from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class CustomUser(models.Model):
    address = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    birthDay = models.DateField(verbose_name="Date of Birth", blank=True, null=True, help_text="This field must be 'YYYY-MM-DD' format")
    user = models.OneToOneField(User)


class UserLocation(models.Model):
    longitude = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
