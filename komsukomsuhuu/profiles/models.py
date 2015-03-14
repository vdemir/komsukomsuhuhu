from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser

# Create your models here.
"""
class MyUser(AbstractBaseUser):
    user = models.ForeignKey(User, unique=True)
    customs = models.CharField(max_length=200)

    def __unicode__(self):
        return self.email


class user_profile(AbstractBaseUser):


    custom_field = models.CharField(blank=True, max_length=100)

    def __unicode__(self):
        return self.user
"""
"""

class MyUser(AbstractBaseUser):
    user = models.ForeignKey(User, unique=True)
    customs = models.CharField(max_length=100)

"""
