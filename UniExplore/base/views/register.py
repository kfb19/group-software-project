from ..forms import UserRegisterForm
from ..models import Profile
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import Group

"""
    Authors: Conor Behard Roberts
    Description: Checks to see if an email is valid given a valid suffix
"""


def is_valid_email(email, valid_suffix):
    ending = email.split('@')[1].lower()
    return valid_suffix.lower() == ending


"""
    Authors: Michael Hills, Conor Behard Roberts
    Description: Function for user registration
"""


def registerPage(request):

    # Getting form from forms.py
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        # Save form if it is valid
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username').lower().capitalize()

            try:
                User.objects.get(username=username)
            except BaseException:
                if is_valid_email(email, settings.EMAIL_EXTENSION):
                    try:
                        # Check to see if there is already a user with the same email registered
                        User.objects.get(email=email)
                    except BaseException:
                        user = form.save()
                        user.backend = 'django.contrib.auth.backends.ModelBackend'  # Sets the backend authenticaion model

                        Profile.objects.create(
                            user=user,
                            name=username,
                        )
                        # Adds the user to the user group
                        group = Group.objects.get(name='user')
                        user.groups.add(group)

                        login(request, user)
                        messages.success(request, f'Account created for {username}!')
                        return redirect('home')

                    messages.warning(request, "A User with this email already exists")
                    return redirect('register')
                else:
                    messages.warning(request, "Must sign up with an email ending in exeter.ac.uk")
                    return redirect('register')
            messages.warning(request, "This username is taken")
            return redirect('register')
    context = {'form': form}
    return render(request, 'base/login_register.html', context)
