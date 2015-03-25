__author__ = 'erkoc'

from django import forms
from models import Group


class GroupForm(forms.ModelForm):

    class Meta:
        fields = ['name', 'type', 'isActive']
        model = Group