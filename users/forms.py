from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(label='netID')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='netID')


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField(label='netID')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name']

