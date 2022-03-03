"""
Authors:
    - Michael Hills
    - Kate Belson
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Challenges, Responses, Profile


# Form for user registrations (Michael Hills)
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Form for challenges to be added (Michael Hills)
class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenges
        fields = ['category','name','points','description','lat','long']
        widgets = {'lat': forms.HiddenInput(), 'long':forms.HiddenInput}



# Form for responding to a challenge (Michael Hills)
class ResponseForm(forms.ModelForm):
    class Meta:
        model = Responses
        fields = ['description']


class ProfileForm(ModelForm):
    class Meta:
        model = Challenges
        fields = '__all__'


# Form for updating profile
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'bio', 'university', 'picture']
