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
# import folium
import json

# def add_location(map, location, popup):
#     #tooltip
#     tooltip = 'Click for more info'
#     folium.Marker(location, popup, tooltip=tooltip).add_to(map)
#     return map

# Function to open and return a json file 
def open_json_file(file_name):
    file = open(file_name)
    return json.load(file)


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

    locations = open_json_file('base/resources/latLong.json')
    # Adds markers to the map for each location
    for location in locations:
        coords = [location['lat'], location['long']]
        popup = location['locationName']
        map = add_location(map, coords, popup)

    map = map._repr_html_()
    categories = Category.objects.all()
    challenges = Challenges.objects.all()

    context = {'categories':categories,'challenges':challenges, 'map':map}

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