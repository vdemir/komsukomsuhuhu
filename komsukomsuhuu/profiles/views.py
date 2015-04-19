from django.shortcuts import render_to_response, HttpResponseRedirect, redirect, get_object_or_404 ,get_list_or_404
from django.template import RequestContext
from django.contrib.auth import login as auth_login, logout as auth_logout
from profiles.forms import LoginForm, AdvancedRegistrationForm
from django.contrib.auth.decorators import login_required
from profiles.models import CustomUser
from profiles.forms import ChangeCustomUserDetails
from messages.forms import NewMessageForm
from groups.models import Group
from entities.models import Topic
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from elasticsearch import Elasticsearch
# Create your views here.

es = Elasticsearch()

@login_required(login_url='/login')
def home(request):
    notifications = request.user.notifications.unread().order_by('-timestamp')

    return render_to_response('home.html', {
        'notifications': notifications
    }, RequestContext(request))

def register(request):
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
            return HttpResponseRedirect("/../login")
    else:
        form = AdvancedRegistrationForm()
    return render_to_response("register.html", {
        "form": form,
    }, RequestContext(request))


def login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_login(request, form.user)
            return redirect(reverse("home"))

    return render_to_response("login.html", {
        "form": form
    },  RequestContext(request))

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


def users(request, username):
    user = get_object_or_404(User, username=username)
    form = NewMessageForm()

    return render_to_response("users.html", {
        'user': user,
        'form': form,
    }, RequestContext(request))


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    fav_groups = list(Group.objects.filter(user_favorited=user))
    fav_topics = list(Topic.objects.filter(user_favorited=user))
    my_groups = list(Group.objects.filter(members=user))

    favgroups_showmore = True if len(fav_groups) > 5 else False
    favtopic_showmore = True if len(fav_topics) > 5 else False
    mygroups_showmore = True if len(my_groups) > 5 else False

    return render_to_response("profile.html", {
        'user': user,
        'fav_groups': fav_groups[:5],
        'my_groups': my_groups[:5],
        'fav_topics': fav_topics[:5],
        'favgroups_showmore' : favgroups_showmore,
        'favtopic_showmore' : favtopic_showmore,
        'mygroups_showmore' : mygroups_showmore,
    }, RequestContext(request))


def search(request):
    q = request.GET['q']
    value = es.search(index='komsukomsuhuu', q=q)
    if value['hits']['total']:
        data = User.objects.get(username=value['hits']['hits'][0]['_source']['username'])
        return render_to_response("result.html", {
            "data": data
        }, RequestContext(request))
    else:
         return render_to_response("result.html", {
        }, RequestContext(request))