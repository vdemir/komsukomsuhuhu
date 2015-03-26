__author__ = 'erkoc'

from django import forms
from models import Topic
from models import Post


class TopicForm(forms.ModelForm):

    class Meta:
        fields = ['title', 'content']
        model = Topic


class PostForm(forms.ModelForm):

    class Meta:
        fields = ['content']
        model = Post