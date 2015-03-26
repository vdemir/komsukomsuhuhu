from django.shortcuts import HttpResponse, render_to_response, HttpResponseRedirect, redirect
from django.template import RequestContext
from django.contrib.auth import login as auth_login, logout as auth_logout
from profiles.forms import LoginForm, AdvancedRegistrationForm
from django.contrib.auth.decorators import login_required
from profiles.models import CustomUser
from profiles.forms import ChangeCustomUserDetails
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
# Create your views here.


def home(request):
        return render_to_response('index.html', {
            }, RequestContext(request))


def register(request):
    if request.method == 'POST':
        form = AdvancedRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            created_user = User.objects.get(username=form.cleaned_data['username'])
            blank_customuser = CustomUser(user=created_user)
            blank_customuser.save()
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
        return redirect(reverse("groups"))

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


def logout(request):
    auth_logout(request)
    return render_to_response("logout.html", {}, RequestContext(request))

