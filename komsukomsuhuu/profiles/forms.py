from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
#from profiles.models import MyUser


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if not username or not password:
            return self.cleaned_data
        user = authenticate(username=username, password=password)

        if user:
            self.user = user
        else:
            raise ValidationError('Wrong username or password !')

        return self.cleaned_data


class RegistrationForm(UserCreationForm):
    pass


class AdvancedRegistrationForm(UserCreationForm):
    #customfield = forms.CharField(max_length=200)
    class Meta:
        model = User

        fields = ('first_name', 'last_name', 'username', 'email')

 
    def clean_email(self):
        if not self.cleaned_data['email']:
            raise forms.ValidationError(u'Enter email.')
 
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(
                u'''
                This email has already been in use. Please try with different email.
                '''
            )
        return self.cleaned_data['email']


"""
class AdvancedRegistrationForm(UserCreationForm):


    customs = forms.CharField(max_length=100)

    class Meta:
        model = User

        fields = ('first_name', 'last_name', 'username', 'email', 'customs')

    def save(self, commit=True):
        user = super(AdvancedRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
"""

"""
class AdvancedRegistrationForm(UserCreationForm):

    #customs = forms.CharField(widget=forms.widget.TextInput, label="Customss", max_length=100)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', ]

    def clean(self):

        cleaned_data = super(AdvancedRegistrationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(AdvancedRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        #user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
"""
