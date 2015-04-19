from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Group(models.Model):
    TYPE_CHOICES = (
        (1, 'Public'),
        (2, 'Private'),
    )
    STATE_CHOICES = (
        (1, 'Permanent'),
        (2, 'Temporary'),
    )
    RANGE_CHOICES = (
        (1, '1 KM'),
        (2, '2 KM'),
        (3, '3 KM'),
        (4, '4 KM'),
        (5, '5 KM'),
    )
    name = models.CharField(max_length=100)
    type = models.IntegerField(choices=TYPE_CHOICES, default=1)
    state = models.IntegerField(choices=STATE_CHOICES, default=1)
    range = models.IntegerField(choices=RANGE_CHOICES, default=1)
    manager = models.ForeignKey(User, related_name='manager')
    members = models.ManyToManyField(User, related_name='members')
    isActive = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateField(auto_now=True)
    user_favorited = models.ManyToManyField(User, related_name='favorite_groups')

    def __unicode__(self):
        return "%s" % (self.name)


class GroupLocation(models.Model):
    group = models.OneToOneField(Group)
    longitude = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)

    def __unicode__(self):
        return "Group id: %s-Longitude: %s-Latitude: %s" % (self.group.id, self.longitude, self.latitude)
