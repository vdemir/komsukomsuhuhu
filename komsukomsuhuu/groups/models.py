from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Group(models.Model):
    PUBLIC = 1
    PRIVATE = 2
    TYPE_CHOICES = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
    )
    name = models.CharField(max_length=100)
    type = models.IntegerField(choices=TYPE_CHOICES, default=PUBLIC)
    manager = models.ForeignKey(User, related_name='manager')
    members = models.ManyToManyField(User, related_name='members')
    isActive = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateField(auto_now=True)

    def __unicode__(self):
        return "%s - %s" % (self.name, self.manager)

