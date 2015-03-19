from django.shortcuts import render_to_response, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from models import Topic, Post
from forms import TopicForm, PostForm
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


@login_required(login_url='/login')
def new_post(request, pk):
    form = PostForm()
    topic = Topic.objects.get(id=pk)
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            form.instance.owner = request.user
            form.instance.topic = topic
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render_to_response('detail_topic.html', {}, RequestContext(request))


@login_required(login_url='/login')
def detail_topic(request, pk):
    topic = get_object_or_404(Topic, id=pk)
    posts = Post.objects.filter(topic=pk)

    return render_to_response('detail_topic.html', {
        'topic': topic,
        'posts': posts
    }, RequestContext(request))