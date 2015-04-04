__author__ = 'erkoc'

from django import forms
from models import Group, GroupLocation


class GroupForm(forms.ModelForm):

    class Meta:
        fields = ['name', 'type', 'state', 'range', 'isActive']
        model = Group


class GroupLocationForm(forms.ModelForm):

    class Meta:
        fields = ['longitude', 'latitude']
        model = GroupLocation