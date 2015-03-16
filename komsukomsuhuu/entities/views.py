from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from models import Topic
from forms import TopicForm
from groups.models import Group
# Create your views here.


@login_required(login_url='/login')
def list_topics(request, pk):
    topics = Topic.objects.get(id=pk)
    return render_to_response("detail_group.html", {
        'topics': topics
    }, RequestContext(request))

@login_required(login_url='/login')
def new_topic(request, pk):
    group = Group.objects.get(id=pk)
    form = TopicForm()

    if request.method == 'POST':
        form = TopicForm(request.POST)

        if form.is_valid():
            form.instance.owner = request.user
            form.instance.group = group
            form.save()
            return redirect(reverse("groups"))

    return render_to_response('new_topic.html', {
        'form': form,
        'group': group,
    }, RequestContext(request))