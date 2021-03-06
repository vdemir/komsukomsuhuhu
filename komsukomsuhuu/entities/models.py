from django.db import models
from django.contrib.auth.models import User
from groups.models import Group
from django.utils import timezone
# Create your models here.


class Topic(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    owner = models.ForeignKey(User, related_name='topic_owner')
    group = models.ForeignKey(Group, related_name='group')
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateField(auto_now=True)
    user_favorited = models.ManyToManyField(User, related_name='favorite_topic')

    def __unicode__(self):
        return "%s - %s" % (self.title, self.group)


class Post(models.Model):
    content = models.TextField()
    owner = models.ForeignKey(User, related_name='post_owner')
    topic = models.ForeignKey(Topic, related_name='topic')
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateField(auto_now=True)
    user_displayed_posts = models.ManyToManyField(User, related_name="read_posts")

    def __unicode__(self):
        return "%s - %s" % (self.topic.title, self.owner)