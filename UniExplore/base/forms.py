from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Challenges, Responses


# Form for user registrations
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Form for challenges to be added
class ChallengeForm(ModelForm):
    class Meta:
        model = Challenges
        fields = '__all__'


# Form for responding to a challenge
class ResponseForm(ModelForm):
    class Meta:
        model = Responses
        fields = ['description']

# Form to create a profile
class ProfileForm(ModelForm):
    class Meta:
        model = Challenges
        fields = '__all__'
