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
from groups.tasks import create_temp_group, destroy_temp_group
from datetime import datetime, timedelta
from functions.function import info

db = Connection()['komsukomsuhuu']

# Create your views here.



@login_required(login_url='/login')
def list_groups(request):
    groups = Group.objects.filter(isActive=True)

    return render_to_response('groups.html', {
        'favorited_groups': info(request)[0],
        'favorited_topics': info(request)[1],
        'notifications': info(request)[2],
        'inbox_notifications': info(request)[3],
        'groups': groups
    }, RequestContext(request))


@login_required(login_url='/login')
def list_groups_on_map(request):
    groups = Group.objects.filter(isActive=True)
    return render_to_response('maps.html', {
        'favorited_groups': info(request)[0],
        'favorited_topics': info(request)[1],
        'notifications': info(request)[2],
        'inbox_notifications': info(request)[3],
        'groups': groups,
        'length': len(groups)
    }, RequestContext(request))


@login_required(login_url='/login')
def new_group(request):
    form = GroupForm()
    form_location = GroupLocationForm()
    if request.method == 'POST':
        form = GroupForm(request.POST)
        form_location = GroupLocationForm(request.POST)
        if form.is_valid() and form_location.is_valid():
            form.instance.manager = request.user
            form.save()
            # TODO our group names not unique!! get by name fails if there are 2 groups with same name
            group = Group.objects.get(name=form.cleaned_data['name'])
            group.members.add(request.user)
            group.save()
            form_location.instance.group = group
            form_location.save()
            try:
                data = {
                    'group': group.id,
                    'type': 'Point',
                    'coordinates': (
                        float(form_location.cleaned_data['longitude']), float(form_location.cleaned_data['latitude'])),
                }
                db.location.insert(data)

                if group.state == 2:
                    create_temp_group.apply_async(args=[group.id, ],
                                                  eta=datetime.utcnow() + timedelta(hours=group.duration),
                                                  link=destroy_temp_group.s())
            except Exception:
                return HttpResponse("Something is wrong")
            return redirect(reverse('groups'))

        else:
            return HttpResponse('Form is not valid')

    return render_to_response('new_group.html', {
        'form': form
    }, RequestContext(request))


@login_required(login_url='/login')
def delete_group(request, pk):
    group = Group.objects.get(id=pk, manager=request.user)
    group.isActive = False
    group.save()

    return redirect(reverse('home'))


@login_required(login_url='/login')
def detail_group(request, pk):
    group = get_object_or_404(Group, id=pk)
    topics = Topic.objects.filter(group=pk)
    form = UserLocationForm()
    if request.method == "POST":
        form = UserLocationForm(request.POST)
        if form.is_valid():
            try:
                longitude = float(form.cleaned_data['longitude'])
                latitude = float(form.cleaned_data['latitude'])
                data = {
                    'group': group.id,
                    'coordinates':
                        SON([('$near', [longitude, latitude]), ('$maxDistance', group.range / 111.12)])}
                if list(db.location.find(data)):
                    group.members.add(request.user)
                    # return redirect(reverse('groups'))
                    return HttpResponse("ekleme gerceklesti.")
                else:
                    return HttpResponse("ekleyemedik.")
            except Exception:
                return HttpResponse("Something is wrong")

    unread_notifications = request.user.notifications.unread()

    for unread_notification in unread_notifications:
        if unread_notification.target == group:
            unread_notification.mark_as_read()
            unread_notification.level = "info"
            unread_notification.save()

    return render_to_response('detail_group.html', {
        'favorited_groups': info(request)[0],
        'favorited_topics': info(request)[1],
        'notifications': info(request)[2],
        'inbox_notifications': info(request)[3],
        'group': group,
        'topics': topics,
        'user': request.user,
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
    if request.user in group.members.all():
        if Group.objects.filter(id=pk, user_favorited=request.user).exists():
            group.user_favorited.remove(request.user)
        else:
            group.user_favorited.add(request.user)
    return redirect(reverse('groups'))
    return HttpResponse("You are not member of this group")


@login_required(login_url='/login')
def show_neighbours(request):
    groupList = []
    neighbourList = []
    groups = Group.objects.all()
    for group in groups:
        if group.members.filter(username=request.user.username):
            groupList.append(group)
    for myGroup in groupList:
        myNeighs = myGroup.members.all()
        if myNeighs.exists():
            for myNeigh in myNeighs:
                if not (myNeigh == request.user or myNeigh in neighbourList):
                    neighbourList.append(myNeigh)
    return render_to_response("neighbours.html", {
        'favorited_groups': info(request)[0],
        'favorited_topics': info(request)[1],
        'notifications': info(request)[2],
        'inbox_notifications': info(request)[3],
        'mygroups': groupList,
        'myneighs': neighbourList,
    }, RequestContext(request))

