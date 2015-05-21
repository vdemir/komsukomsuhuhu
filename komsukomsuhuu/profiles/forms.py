from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from profiles.models import CustomUser, UserLocation


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
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

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


class ChangeCustomUserDetails(forms.ModelForm):

    class Meta:
        model = CustomUser

        fields = ('address', 'phone', 'birthDay')


class UserLocationForm(forms.ModelForm):

    class Meta:
        model = UserLocation

        fields = ['longitude', 'latitude']


class UserStatusForm(forms.ModelForm):

    class Meta:
        model = CustomUser

        fields = ('status',)
