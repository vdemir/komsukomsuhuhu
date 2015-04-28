__author__ = 'erkoc'

from groups.models import Group
from entities.models import Topic


def info(request):
    favorited_groups = list(Group.objects.filter(user_favorited=request.user))
    favorited_topics = list(Topic.objects.filter(user_favorited=request.user))
    inbox_notifications = []
    other_notifications = []

    unread_notifications = request.user.notifications.unread()

    for notification in unread_notifications:
        notification.level = "warning"
        notification.save()

    notifications = request.user.notifications.order_by('-timestamp')

    for notification in notifications:
        if notification.verb in ('sent new message to you','created new conversation'):
            inbox_notifications.append(notification)
        else:
            other_notifications.append(notification)

    return [favorited_groups, favorited_topics, other_notifications, inbox_notifications]