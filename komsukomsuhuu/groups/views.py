from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from models import Group
from forms import GroupForm, GroupLocationForm
from profiles.forms import UserLocationForm
from entities.models import Topic
from pymongo import Connection
from bson import SON

db = Connection()['komsukomsuhuu']

# Create your views here.

# TODO temporary icin cozum getirilecek

@login_required(login_url='/login')
def list_groups(request):
    groups = Group.objects.all()

    return render_to_response('groups.html', {
        'groups': groups
    }, RequestContext(request))

@login_required(login_url='/login')
def list_groups_on_map(request):
    groups = Group.objects.all()
    return render_to_response('maps.html', {
        'groups': groups,
        'length': len(groups)
    }, RequestContext(request))



@login_required(login_url='/login')
def new_group(request):
    # TODO range set edilecek
    form = GroupForm()
    form_location = GroupLocationForm()
    if request.method == 'POST':
        form = GroupForm(request.POST)
        form_location = GroupLocationForm(request.POST)
        if form.is_valid() and form_location.is_valid():
            form.instance.manager = request.user
            form.save()
            group = Group.objects.get(name=form.cleaned_data['name'])
            form_location.instance.group = group
            form_location.save()
            data = {
                 'group': group.id,
                 'type': 'Point',
                 'coordinates': (float(form_location.cleaned_data['longitude']), float(form_location.cleaned_data['latitude'])),
            }
            db.location.insert(data)
            return redirect(reverse('home'))

    return render_to_response('new_group.html', {
        'form': form
    }, RequestContext(request))


@login_required(login_url='/login')
def delete_group(request, pk):
    Group.objects.filter(id=pk, manager=request.user).delete()

    return redirect(reverse('home'))


@login_required(login_url='/login')
def detail_group(request, pk):
    group = get_object_or_404(Group, id=pk)
    topics = Topic.objects.filter(group=pk)
    form = UserLocationForm()

    if request.method == "POST":
        form = UserLocationForm(request.POST)
        if form.is_valid():
            longitude = float(form.cleaned_data['longitude'])
            latitude = float(form.cleaned_data['latitude'])
            data = {
                'group': group.id,
                'coordinates':
                    SON([('$near', [longitude, latitude]), ('$maxDistance', group.range/111.12)])}
            if list(db.location.find(data)):
                group.members.add(request.user)
                #return redirect(reverse('groups'))
                return HttpResponse("ekleme gerceklesti.")
            else:
                return HttpResponse("ekleyemedik.")

    unread_notifications = request.user.notifications.unread()

    for unread_notification in unread_notifications:
        if unread_notification.target == group:
            unread_notification.mark_as_read()
            unread_notification.level="info"
            unread_notification.save()

    return render_to_response('detail_group.html', {
        'group': group,
        'topics': topics,
    }, RequestContext(request))


@login_required(login_url='/login')
def edit_group(request, pk):
    if Group.objects.get(id=pk).manager != request.user:
        return HttpResponse("Only owner can edit")
    group = Group.objects.get(id=pk, manager=request.user)
    form = GroupForm(instance=group)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect(reverse('groups'))

    return render_to_response('edit_group.html', {
        'form': form,
        'group': group,
    }, RequestContext(request))

@login_required(login_url='/login')
def join_group(request, pk):
    group = Group.objects.get(id=pk)
    if Group.objects.filter(id=pk, members=request.user).exists():
        group.members.remove(request.user)
    else:
        group.members.add(request.user)
    return redirect(reverse('groups'))

@login_required(login_url='/login')
def favorite_group(request, pk):
    group = Group.objects.get(id=pk)
    if Group.objects.filter(id=pk, user_favorited=request.user).exists():
        group.user_favorited.remove(request.user)
    else:
        group.user_favorited.add(request.user)
    return redirect(reverse('groups'))


