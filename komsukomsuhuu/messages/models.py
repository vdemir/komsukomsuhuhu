from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_unicode

# Create your models here.


class Conversation(models.Model):
    users = models.ManyToManyField(User, related_name="conversations")
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"

    def __unicode__(self):
        username_list = self.users.values_list("username", flat=True)
        return smart_unicode('Conversation: %s' % ','.join(username_list))


class Message(models.Model):
    conversation = models.ForeignKey('Conversation', related_name="messages")
    sender = models.ForeignKey(User, related_name="sent_messages")
    date_sent = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    seen_users = models.ManyToManyField(User, related_name="seen_meesages")

    def __unicode__(self):
        return smart_unicode("Message sender: %s" % self.sender.username)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"