__author__ = 'erkoc'

from django import forms
from models import Group, GroupLocation


class GroupForm(forms.ModelForm):

    class Meta:
        fields = ['name', 'type', 'isActive']
        model = Group


class GroupLocationForm(forms.ModelForm):

    class Meta:
        field = ['longitude', 'latitude']
        model = GroupLocation