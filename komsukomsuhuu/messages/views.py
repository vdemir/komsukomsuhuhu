from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from messages.forms import NewMessageForm
from messages.models import Conversation, Message
from django.contrib.auth.decorators import login_required
from notifications import notify
from functions.function import info


def send_notification(sender, recipient_username, verb, target):
    if recipient_username:
        notify.send(
            sender,
            recipient=recipient_username,
            verb=verb,
            target=target,
        )


@login_required(login_url='/login')
def new_message(request, username):
    user = get_object_or_404(User, username=username)

    form = NewMessageForm(request.POST)

    if form.is_valid():
        text = form.cleaned_data.get("text")

        conversation = Conversation.objects.create()
        conversation.users.add(request.user)
        conversation.users.add(user)

        message = conversation.messages.create(
            text=text,
            sender=request.user,
        )

        message.seen_users.add(request.user)

        send_notification(request.user, user, "created new conversation", conversation)

        redirect_to = "%(path)s?message_sent=success" % {
            "path": reverse("inbox")
        }

        return redirect(redirect_to)

    redirect_to = "%(path)s?message_sent=error" % {
        "path": reverse("inbox")
    }

    return redirect(redirect_to)


@login_required(login_url='/login')
def inbox(request):
    conversations = Conversation.objects.filter(
        users=request.user,
    ).annotate(
        message_count=models.Count("messages")
    ).exclude(
        message_count=0
    ).order_by(
        "-date_created"
    )
    message_sent = request.GET.get("message_sent")

    return render_to_response("inbox.html", {
        'favorited_groups': info(request)[0],
        'favorited_topics': info(request)[1],
        'notifications': info(request)[2],
        'inbox_notifications': info(request)[3],
        'conversations': conversations,
        'message_sent': message_sent
    }, RequestContext(request))


@login_required(login_url='/login')
def conversation_detail(request, pk):
    conversation = get_object_or_404(
        Conversation, users=request.user, id=pk)

    users = list(conversation.users.all())

    if users[0] == request.user:
        recipent = users[1]
    elif users[0] != request.user:
        recipent = users[0]
    else:
        return

    messages = conversation.messages.all()

    form = NewMessageForm()

    if request.method == "POST":
        form = NewMessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data.get("text")

            conversation.messages.create(
                sender=request.user,
                text=message)

            form = NewMessageForm()

            send_notification(request.user, recipent, "sent new message to you", conversation)

    # mark as seen current messages
    unread_messages = Message.objects.filter(
        conversation=conversation
    ).exclude(
        seen_users=request.user
    )

    for message in unread_messages:
        message.seen_users.add(request.user)

    unread_notifications = request.user.notifications.unread()

    for unread_notification in unread_notifications:
        if unread_notification.target == conversation:
            unread_notification.mark_as_read()
            unread_notification.level = "info"
            unread_notification.save()

    return render_to_response("conversation_detail.html", {
        'favorited_groups': info(request)[0],
        'favorited_topics': info(request)[1],
        'notifications': info(request)[2],
        'inbox_notifications': info(request)[3],
        "conversation": conversation,
        "messages": messages,
        "form": form,
        "other_party": recipent,
    }, RequestContext(request))