"""
Authors:
    - Michael Hills
    - Kate Belson
    - Lucas Smith
    - Conor Behard Roberts
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Challenges, Responses, Profile


# Form for user registrations (Michael Hills, Conor Behard Roberts)
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


# Form for challenges to be added (Michael Hills, Tomas Premoli)
class DateTimeInput(forms.DateInput):
    input_type = 'datetime-local'

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenges
        fields = ['category', 'name', 'points', 'description', 'lat', 'long', 'expires_on']
        widgets = {'lat': forms.HiddenInput(), 'long': forms.HiddenInput, 'expires_on': DateTimeInput()}


# Form for responding to a challenge (Michael Hills)
class ResponseForm(forms.ModelForm):
    class Meta:
        model = Responses
        fields = ['description', 'photograph']


class ProfileForm(ModelForm):
    class Meta:
        model = Challenges
        fields = '__all__'


# Forms for updating profile (Lucas, Conor Behard Roberts)
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField

    class Meta:
        model = User
        fields = ['username']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'university', 'picture']
