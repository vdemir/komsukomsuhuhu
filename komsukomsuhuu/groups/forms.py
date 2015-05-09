__author__ = 'erkoc'

from django import forms
from models import Group, GroupLocation


class GroupForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'type', 'state', 'range', 'duration', 'enrollment_key']
        model = Group


class EditGroupForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'type', 'range']
        model = Group


class GroupLocationForm(forms.ModelForm):
    class Meta:
        fields = ['longitude', 'latitude']
        model = GroupLocation


class CheckEnrollmentKey(forms.ModelForm):
    class Meta:
        fields = ['enrollment_key']
        model = Group
