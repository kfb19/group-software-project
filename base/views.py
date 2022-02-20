from email import message
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ChallengeForm, UserRegisterForm
from .models import Category, Challenges
from django.db.models import Q
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect


#view for the main homepage
def home(request):
    
    #select all categories
    categories = Category.objects.all()

    #get the filter from the ?q= in the URL
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    #filter the challenges by q
    challenges = Challenges.objects.filter(
        Q(category__name__icontains=q))

    #variables to pass to the database
    context = {'categories':categories,'challenges':challenges}

    return render(request,'base/home.html',context)


#view for logging in
def loginPage(request):

    #allows us to change the page based on if a user is logged in
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')


    #get info from html form
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


#logout user
def logoutUser(request):

    logout(request)
    return redirect('home')


#user registration
def registerPage(request):
    
    #getting form from forms.py
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        #save form if it is valid
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request,user)
            messages.success(request, f'Account created for {username}!')
            return redirect('home')



    context = {'form': form}
    return render(request, 'base/login_register.html',context)



@login_required(login_url='/login')
def userProfile(request):
    return render(request, 'base/profile.html',{})


#create challenge
def createChallenge(request):
    form = ChallengeForm()
    if request.method == 'POST':
        form = ChallengeForm(request.POST)

        #if valid challenge, add to database
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'base/createChallenge.html',context)

