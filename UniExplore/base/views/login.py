from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

"""
    Authors: Michael Hills
    Description: View for logging in
"""
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
        except BaseException:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # Sets the backend authenticaion model
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


"""
    Authors: Michael Hills
    Description: Function to log the user out 
"""
def logoutUser(request):
    logout(request)
    return redirect('home')