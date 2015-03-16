from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from models import Group
from forms import GroupForm
from entities.models import Topic
# Create your views here.


def list_groups(request):
    groups = Group.objects.all()
    return render_to_response('groups.html', {
        'groups': groups
    }, RequestContext(request))


@login_required(login_url='/login')
def new_group(request):
    form = GroupForm()

    if request.method == 'POST':
        form = GroupForm(request.POST)

        if form.is_valid():
            form.instance.manager = request.user
            form.save()
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
    group.members.add(request.user)
    return redirect(reverse('groups'))