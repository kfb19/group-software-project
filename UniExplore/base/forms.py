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
class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenges
        fields = ['category','name','points','description','lat','long']
        widgets = {'lat': forms.HiddenInput(), 'long':forms.HiddenInput}
        


# Form for responding to a challenge
class ResponseForm(forms.ModelForm):
    class Meta:
        model = Responses
        fields = ['description']

# Form to create a profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Challenges
        fields = '__all__'
