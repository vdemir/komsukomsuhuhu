from django.shortcuts import render_to_response, HttpResponseRedirect, redirect, get_object_or_404, get_list_or_404, \
    render, HttpResponse
from django.template import RequestContext
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from profiles.forms import LoginForm, AdvancedRegistrationForm
from django.contrib.auth.decorators import login_required
from profiles.models import CustomUser
from profiles.forms import ChangeCustomUserDetails, UserStatusForm
from messages.forms import NewMessageForm
from groups.models import Group
from entities.models import Topic
from django.contrib.auth.models import User
from elasticsearch import Elasticsearch
from django.core.urlresolvers import reverse
from functions.function import info
from django.core.mail import EmailMultiAlternatives
from komsukomsuhuu import settings
from django.template.loader import get_template
from django.template import Context

es = Elasticsearch()


@login_required(login_url='/login')
def home(request):
    latest_post = []
    groups = request.user.members.all()
    for group in groups:
        for topic in group.group.all():
            for post in topic.topic.all():
                latest_post.append(post)

    if request.method == 'POST':
        form = UserStatusForm(request.POST, instance=request.user.customuser)
        if form.is_valid():
            form.save()

    latest_post = latest_post[::-1]
    return render_to_response('home.html', {
        'favorited_groups': info(request)[0],
        'favorited_topics': info(request)[1],
        'notifications': info(request)[2],
        'inbox_notifications': info(request)[3],
        'lates_post': latest_post
    }, RequestContext(request))


def register(request):
    register_fail = request.GET.get('register_fail')
    if request.method == 'POST':
        form = AdvancedRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            created_user = User.objects.get(username=form.cleaned_data['username'])
            blank_customuser = CustomUser(user=created_user)
            blank_customuser.save()
            es.index(index='komsukomsuhuu', doc_type='users', body={
                'name': created_user.get_full_name(),
                'username': created_user.username
            })
            plaintext = get_template('registration_email.txt')
            html_template = get_template('registration_email.html')
            d = Context({'full_name': created_user.get_full_name()})
            subject = 'Welcome to KomsuKomsuHuu'
            from_email = settings.DEFAULT_FROM_EMAIL
            to = created_user.email
            text_content = plaintext.render(d)
            html_content = html_template.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect(reverse("home"))

        else:
            redirect_to = "%(path)s?register_fail=true" % {
                "path": reverse("register")
            }
            return redirect(redirect_to)
    else:
        form = AdvancedRegistrationForm()
    return render_to_response("register.html", {
        "form": form,
        "register_fail": register_fail
    }, RequestContext(request))


def login(request):
    register_success = request.GET.get('register_success')
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_login(request, form.user)
            return redirect(reverse("home"))

    return render_to_response("login.html", {
        "form": form,
        "register_success": register_success,
    }, RequestContext(request))


@login_required(login_url='/login')
def edit_profile(request):
    form = ChangeCustomUserDetails(instance=request.user.customuser)
    if request.method == 'POST':
        form = ChangeCustomUserDetails(request.POST, instance=request.user.customuser)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/..")

    return render_to_response('edit_profile.html', {
        'form': form,
    }, RequestContext(request))


@login_required(login_url='/login')
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/../login")


@login_required(login_url='/login')
def users(request, username):
    user = get_object_or_404(User, username=username)
    if user == request.user:
        return user_profile(request)
    else:
        form = NewMessageForm()

        return render_to_response("users.html", {
            'users': user,
            'form': form,
            'favorited_groups': info(request)[0],
            'favorited_topics': info(request)[1],
            'notifications': info(request)[2],
            'inbox_notifications': info(request)[3],
        }, RequestContext(request))


@login_required(login_url='/login')
def user_profile(request):
    fav_groups = list(Group.objects.filter(user_favorited=request.user))
    fav_topics = list(Topic.objects.filter(user_favorited=request.user))
    my_groups = list(Group.objects.filter(members=request.user))

    return render_to_response("profile.html", {
        'favorited_groups': info(request)[0],
        'favorited_topics': info(request)[1],
        'notifications': info(request)[2],
        'inbox_notifications': info(request)[3],
        'user': request.user,
        'fav_groups': fav_groups,
        'my_groups': my_groups,
        'fav_topics': fav_topics,
    }, RequestContext(request))


@login_required(login_url='/login')
def search(request):
    users = []
    try:
        q = request.GET['q']
        value = es.search(index='komsukomsuhuu', q=q)
        if value['hits']['total']:
            for user in value['hits']['hits']:
                users.append(User.objects.get(username=user['_source']['username']))
            return render_to_response("result.html", {
                'favorited_groups': info(request)[0],
                'favorited_topics': info(request)[1],
                'notifications': info(request)[2],
                'inbox_notifications': info(request)[3],
                'users': users
            }, RequestContext(request))
        else:
            return render_to_response("result.html", {
                'favorited_groups': info(request)[0],
                'favorited_topics': info(request)[1],
                'notifications': info(request)[2],
                'inbox_notifications': info(request)[3],
            }, RequestContext(request))
    except Exception:
        return HttpResponse("Something is wrong!")


@login_required(login_url='/login')
def notifications(request):
    notifications = []
    unread_notifications = request.user.notifications.unread()

    for notification in unread_notifications:
        notification.level = "warning"
        notification.save()

    all_notifications = request.user.notifications.order_by('-timestamp')

    for notification in all_notifications:
        if notification.verb not in ('sent new message to you', 'created new conversation'):
            notifications.append(notification)

    return render_to_response('notifications.html', {
        'favorited_groups': info(request)[0],
        'favorited_topics': info(request)[1],
        'notifications': info(request)[2],
        'inbox_notifications': info(request)[3],
        'notifications': notifications
    }, RequestContext(request))

