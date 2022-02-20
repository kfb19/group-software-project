from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Challenges


#form for user registrations
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']




#form for challenges to be added
class ChallengeForm(ModelForm):
    class Meta:
        model = Challenges
        fields = '__all__'