from django.shortcuts import render,RequestContext,HttpResponse,render_to_response,redirect,HttpResponseRedirect,get_object_or_404, redirect
from forms import *
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from profiles.forms import LoginForm, AdvancedRegistrationForm
# Create your views here.


def home(request):
        return render_to_response('index.html', {
            }, RequestContext(request))


def register(request):

    if request.method == 'POST':
        form = AdvancedRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
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
        return HttpResponseRedirect("/..")

    return render_to_response("login.html", {
        "form": form
    },  RequestContext(request))


def logout(request):
    auth_logout(request)
    return render_to_response("logout.html", {}, RequestContext(request))

