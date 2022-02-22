from email import message
import re
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ChallengeForm, UserRegisterForm, ResponseForm
from .models import Category, Challenges
from django.db.models import Q
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect
import folium, json


def add_location(map, location, popup):
    #tooltip
    tooltip = 'Click for more info'
    folium.Marker(location, popup, tooltip=tooltip).add_to(map)
    return map

# Function to open and return a json file 
def open_json_file(file_name):
    file = open(file_name)
    return json.load(file)


# View for the main homepage
def home(request):

    # Map is centred at this location
    center = [50.735805, -3.533051]

    # Map that is bounded to Exeter Uni
    map = folium.Map(location = center,
                 min_lon=-3.520532,
                 max_lon=-3.548116,
                 min_lat=50.729748,
                 max_lat=50.741780,
                 max_bounds=True,
                 zoom_start = 16,
                 min_zoom = 15)

    
    challenge_locations = {}
    challenges = Challenges.objects.all()
    
    #locations = open_json_file('base/resources/latLong.json')
    #print(locations)
    # Adds markers to the map for each location
    for challenge in challenges:
        coords = [challenge.lat, challenge.long]
        popup = challenge.name
        map = add_location(map, coords, popup)
    
    map = map._repr_html_()

    # Select all categories
    categories = Category.objects.all()

    # Get the filter from the ?q= in the URL
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # Filter the challenges by q
    challenges = Challenges.objects.filter(
        Q(category__name__icontains=q))

    # Variables to pass to the database
    context = {'categories':categories,'challenges':challenges, 'map':map}

    return render(request,'base/home.html',context)


# View for logging in
def loginPage(request):

    # Allows us to change the page based on if a user is logged in
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')


    # Get info from html form
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


# Logout usef
def logoutUser(request):

    logout(request)
    return redirect('home')


# User registration
def registerPage(request):
    
    # Getting form from forms.py
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        # Save form if it is valid
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request,user)
            messages.success(request, f'Account created for {username}!')
            return redirect('home')



    context = {'form': form}
    return render(request, 'base/login_register.html',context)


# Only let a user see profile if logged in
@login_required(login_url='/login')
def userProfile(request):
    return render(request, 'base/profile.html',{})


# Create challenge
def createChallenge(request):
    form = ChallengeForm()
    if request.method == 'POST':
        form = ChallengeForm(request.POST)

        # If valid challenge, add to database
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'base/createChallenge.html',context)

@login_required(login_url='/login')
def createResponse(request,pk):
    challenge = Challenges.objects.get(id=pk)
    form = ResponseForm()
    if request.method == 'POST':
        form = ResponseForm(request.POST)

        #If valid response, add to database
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.challenge = challenge

            obj.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'base/createResponse.html',context)

