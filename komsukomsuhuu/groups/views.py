from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from models import Group
from forms import GroupForm, GroupLocationForm, EditGroupForm
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
    delete_group = request.GET.get("delete_group")
    leave_group = request.GET.get("leave_group")
    create_group = request.GET.get("create_group")
    join_group = request.GET.get("join_group")
    error = request.GET.get("error")
    return render_to_response('groups.html', {
        'favorited_groups': info(request)[0],
        'favorited_topics': info(request)[1],
        'notifications': info(request)[2],
        'inbox_notifications': info(request)[3],
        'groups': groups,
        'create_group': create_group,
        'join_group': join_group,
        'leave_group': leave_group,
        'delete_group': delete_group,
        'error': error
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


# TODO Private group icin enrollment key mekanizmasi
@login_required(login_url='/login')
def new_group(request):
    form = GroupForm()
    if request.method == 'POST':
        form = GroupForm(request.POST)
        form_location = GroupLocationForm(request.POST)
        if form.is_valid() and form_location.is_valid():
            form.instance.manager = request.user
            form.save()
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
            redirect_to = "%(path)s?create_group=true" % {
                "path": reverse("groups")
            }
            return redirect(redirect_to)

        else:
            redirect_to = "%(path)s?error=true" % {
                "path": reverse("groups")
            }
            return HttpResponse("Hata var")

    return render_to_response('new_group.html', {
        'form': form
    }, RequestContext(request))


@login_required(login_url='/login')
def delete_group(request, pk):
    group = Group.objects.get(id=pk, manager=request.user)
    group.isActive = False
    group.save()
    redirect_to = "%(path)s?delete_group=true" % {
        "path": reverse("groups")
    }
    return redirect(redirect_to)


@login_required(login_url='/login')
def detail_group(request, pk):
    already_favorited = ''
    key = request.POST.get("key")
    password_fail = request.GET.get("password_fail")
    favorite_group = request.GET.get("favorite_group")
    edit_group = request.GET.get("edit_group")
    join_group = request.GET.get("join_group")
    create_topic = request.GET.get("create_topic")
    group = get_object_or_404(Group, id=pk)
    topics = Topic.objects.filter(group=pk)

    if request.user in group.user_favorited.all():
        already_favorited = True
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
                    if group.type == 1 or key == group.enrollment_key:
                        group.members.add(request.user)
                        # return redirect(reverse('groups'))

                        redirect_to = "%(path)s?join_group=true" % {
                            "path": reverse("detail_group", args=[pk])
                        }
                        return redirect(redirect_to)
                    else:
                        redirect_to = "%(path)s?password_fail=true" % {
                            "path": reverse("detail_group", args=[pk])
                        }
                        return redirect(redirect_to)
                else:
                    redirect_to = "%(path)s?join_group=true" % {
                        "path": reverse("groups")
                    }
                    return redirect(redirect_to)
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
        'create_topic': create_topic,
        'join_group': join_group,
        'edit_group': edit_group,
        'favorite_group': favorite_group,
        'already_favorited': already_favorited,
        'password_fail': password_fail,
    }, RequestContext(request))


@login_required(login_url='/login')
def edit_group(request, pk):
    group = Group.objects.get(id=pk)
    if group.manager != request.user:
        redirect_to = "%(path)s?edit_group=no-permission" % {
            "path": reverse("detail_group", args=[pk])
        }
        return redirect(redirect_to)
    else:
        form = EditGroupForm(instance=group)
        if request.method == 'POST':
            form = EditGroupForm(request.POST, instance=group)
            if form.is_valid():
                form.save()
                redirect_to = "%(path)s?edit_group=permission" % {
                    "path": reverse("detail_group", args=[pk])
                }
                return redirect(redirect_to)

            else:
                HttpResponse("Something is wrong")

    return render_to_response('edit_group.html', {
        'form': form,
        'group': group
    }, RequestContext(request))


@login_required(login_url='/login')
def leave_group(request, pk):
    group = Group.objects.get(id=pk)
    if request.user in group.members.all():
        group.members.remove(request.user)

    redirect_to = "%(path)s?leave_group=true" % {
        "path": reverse("groups")
    }
    return redirect(redirect_to)


@login_required(login_url='/login')
def favorite_group(request, pk):
    group = Group.objects.get(id=pk)
    if request.user in group.members.all():
        if Group.objects.filter(id=pk, user_favorited=request.user).exists():
            group.user_favorited.remove(request.user)
            redirect_to = "%(path)s?favorite_group=leave-success" % {
                "path": reverse("detail_group", args=[pk])
            }
            return redirect(redirect_to)
        else:
            group.user_favorited.add(request.user)
            redirect_to = "%(path)s?favorite_group=success" % {
                "path": reverse("detail_group", args=[pk])
            }
            return redirect(redirect_to)

    redirect_to = "%(path)s?favorite_group=no-members" % {
        "path": reverse("detail_group", args=[pk])
    }
    return redirect(redirect_to)


@login_required(login_url='/login')
def show_neighbours(request):
    group_list = []
    neighbour_list = []
    groups = Group.objects.filter(isActive=True)
    for group in groups:
        if group.members.filter(username=request.user.username):
            group_list.append(group)
    for my_group in group_list:
        my_neighs = my_group.members.all()
        if my_neighs.exists():
            for myNeigh in my_neighs:
                if not (myNeigh == request.user or myNeigh in neighbour_list):
                    neighbour_list.append(myNeigh)
    return render_to_response("neighbours.html", {
        'favorited_groups': info(request)[0],
        'favorited_topics': info(request)[1],
        'notifications': info(request)[2],
        'inbox_notifications': info(request)[3],
        'my_groups': group_list,
        'my_neighs': neighbour_list,
    }, RequestContext(request))