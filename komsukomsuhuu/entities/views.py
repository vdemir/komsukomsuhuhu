from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from models import Topic, Post
from forms import TopicForm, PostForm
from groups.models import Group
from notifications import notify
# Create your views here.


def send_notification(sender, recipient_usernames, verb, target):

    if recipient_usernames:
        for recipient_username in recipient_usernames:
            if recipient_username != sender:
                notify.send(
                    sender,
                    recipient=recipient_username,
                    verb=verb,
                    target=target,
                )


@login_required(login_url='/login')
def list_topics(request, pk):

    topics = Topic.objects.get(id=pk)
    group = topics.group;
    if request.user in group.members.all():
        return render_to_response("detail_group.html", {
            'topics': topics
        }, RequestContext(request))
    return HttpResponse("You are not member of this group")

@login_required(login_url='/login')
def new_topic(request, pk):
    group = Group.objects.get(id=pk)
    form = TopicForm()
    recipient_usernames = group.user_favorited.all()

    if request.user in group.members.all():

        if request.method == 'POST':
            form = TopicForm(request.POST)

            if form.is_valid():
                form.instance.owner = request.user
                form.instance.group = group
                form.save()
                send_notification(request.user, recipient_usernames, 'created new topic on', group)
                return redirect(reverse("groups"))

        return render_to_response('new_topic.html', {
            'form': form,
            'group': group,
        }, RequestContext(request))
    else:
        return HttpResponse("You are not member of this group")


@login_required(login_url='/login')
def new_post(request, pk):
    form = PostForm()
    topic = Topic.objects.get(id=pk)
    group = topic.group;
    if request.user in group.members.all():
        recipient_usernames = topic.user_favorited.all()

        send_notification(request.user, recipient_usernames, 'posted on', topic)

        if request.method == 'POST':
            form = PostForm(request.POST)

            if form.is_valid():
                form.instance.owner = request.user
                form.instance.topic = topic
                form.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        return render_to_response('detail_topic.html', {}, RequestContext(request))
    return HttpResponse("You are not member of this group")


@login_required(login_url='/login')
def detail_topic(request, pk):
    topic = get_object_or_404(Topic, id=pk)
    group = topic.group;
    if request.user in group.members.all():
        posts = Post.objects.filter(topic=pk).order_by('-date_created')

        unread_posts = Post.objects.filter(
            topic=topic
        ).exclude(
            user_displayed_posts=request.user
        )

        for post in unread_posts:
            post.user_displayed_posts.add(request.user)

        unread_notifications = request.user.notifications.unread()

        for unread_notification in unread_notifications:
            if unread_notification.target == topic:
                unread_notification.mark_as_read()
                unread_notification.level="info"
                unread_notification.save()

        return render_to_response('detail_topic.html', {
            'topic': topic,
            'posts': posts
        }, RequestContext(request))
    return HttpResponse("You are not member of this group")

@login_required(login_url='/login')
def favorite_topic(request, pk):
    topic = Topic.objects.get(id=pk)
    group = topic.group;
    if request.user in group.members.all():
        if Topic.objects.filter(id=pk, user_favorited=request.user).exists():
            topic.user_favorited.remove(request.user)
        else:
            topic.user_favorited.add(request.user)
        return HttpResponse("I dont know")
        # TODO Fav Topic - Return
    return HttpResponse("You are not member of this group")



@login_required
def mark_as_read(request):

    request.user.notifications.unread().mark_all_as_read()

    return HttpResponseRedirect(reverse('home'))

