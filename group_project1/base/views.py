from cgitb import reset
from email import message
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from matplotlib.font_manager import json_load
from matplotlib.style import context
from .forms import UserRegisterForm
from .models import Category, Challenges
import json

def home(request):
    
    categories = Category.objects.all()
    challenges = Challenges.objects.all()

    context = {'categories':categories,'challenges':challenges}

    return render(request,'base/home.html',context)

def loginPage(request):

    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    
    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):

    logout(request)
    return redirect('home')

def registerPage(request):
    
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request,user)
            messages.success(request, f'Account created for {username}!')
            return redirect('home')



    context = {'form': form}
    return render(request, 'base/login_register.html',context)

# This successfully receives the post request from the XMLHTTP.
# Need to handle properly, however this is a solid start
def location_get_test(request):
    if request.method == 'POST':
        print(request.body)
        response = HttpResponse()
        return response
    else:
        return render(request, 'base/location_get_test.html/')
    

@login_required(login_url='/login')
def userProfile(request):
    return render(request, 'base/profile.html',{})