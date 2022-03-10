"""
Authors:
    - Michael Hills
    - Conor Behard Roberts
    - Jack Purkiss
    - Kate Belson 
    - Lucas Smith (profile functionality)
"""

from .decorators import allowed_users
from .forms import ChallengeForm, UserRegisterForm, ResponseForm
from .models import Category, Challenges, Likes, Responses, Profile, AccessAttemptAddons
from auth_helper import get_sign_in_flow, get_token_from_code, store_user, remove_user_and_token
from axes.models import AccessAttempt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ChallengeForm, UserRegisterForm, ResponseForm, UserUpdateForm, ProfileUpdateForm
from .models import Category, Challenges, Responses, Profile
from django.core.mail import EmailMessage, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.mail import BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.conf import settings
from auth_helper import get_sign_in_flow, get_token_from_code, store_user, remove_user_and_token
from graph_helper import *
from django.contrib.auth.models import Group
import datetime
import random
import json


"""
    Authors: Conor Behard Roberts
    Description: Function to open and return a json file
"""


def open_json_file(file_name):
    file = open(file_name)
    return json.load(file)


"""
    Authors: Michael Hills
    Description: View for the main homepage
"""


def home(request):
    categories = Category.objects.all()

    # Get the filter from the ?q= in the URL
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    # Get all challenges, not done by the current user
    if request.user.is_authenticated:
        responses = Responses.objects.filter(user=request.user).values_list('challenge_id')

        challenges = Challenges.objects.exclude(id__in=responses).filter(Q(
            category__name__icontains=q)).order_by('-created')
    else:
        challenges = Challenges.objects.filter(Q(
            category__name__icontains=q)).order_by('-created')
        # add locations to map

        # Variables to pass to the database
    context = {'categories': categories, 'challenges': challenges}

    return render(request, 'base/home.html', context)


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


# Logout user
"""
    Authors: Michael Hills
    Description: Function to log the user out 
"""


def logoutUser(request):
    logout(request)
    return redirect('home')


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


"""
    Authors: Lucas Smith
    Description: Profile page with completed tasks
"""


@login_required(login_url='/login')
def userProfile(request):
    responses = Responses.objects.filter(user=request.user).order_by('-created')

    categories = Category.objects.all()
    context = {
        'responses': responses,
        'categories': categories
    }

    return render(request, 'base/profile.html', context)


"""
    Authors: Lucas Smith
    Description: Edit profile page
"""


@login_required(login_url='/login')
def editProfile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            username = user_form.cleaned_data.get('username').lower().capitalize()
            try:
                User.objects.get(username=username)
            except BaseException:
                user_form.save()
                profile_form.save()
                messages.success(request, f'Your account has been updated successfully.')
                return redirect('profile')
            messages.warning(request, "This username already exists")
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'base/profile_edit.html', context)


# See another user's profile
# def profile(request, username):
#   person = User.objects.get(username=username)
#  return render(request, 'base/profile.html', {"person": person})


"""
    Authors: Michael Hills, Jack Purkiss
    Description: Only allow game masters and developers to create challenge
"""


@allowed_users(allowed_roles=["game_master", 'developer'])
def createChallenge(request):
    categories = Category.objects.all()
    form = ChallengeForm()
    if request.method == 'POST':
        form = ChallengeForm(request.POST)

        # If valid challenge, add to database
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('home')
    context = {'form': form, 'categories': categories}
    return render(request, 'base/createChallenge.html', context)


"""
    Authors: Michael Hills
    Description: View to complete a challenge 
"""


@login_required(login_url='/login')
def createResponse(request, pk):
    challenge = Challenges.objects.get(id=pk)
    categories = Category.objects.all()
    form = ResponseForm()
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        # If valid response, add to database
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.challenge = challenge

            obj.save()

            profile = request.user.profile
            profile.points += challenge.points
            profile.save()
            return redirect('home')
    context = {'form': form, 'categories': categories}
    return render(request, 'base/createResponse.html', context)


"""
    Authors: Michael Hills
    Description: View of the leaderboard
"""


def leaderboard(request):

    categories = Category.objects.all()
    profiles = Profile.objects.all().order_by('-points')
    context = {'profiles': profiles, 'categories': categories}
    return render(request, 'base/leaderboard.html', context)


"""
    Authors: Conor Behard Roberts
    Description: Converts timedelta object into a readable string
"""


def strfdelta_round(tdelta, round_period='second'):
    """timedelta to string,  use for measure running time
    attend period from days downto smaller period, round to minimum period
    omit zero value period
    """
    period_names = ('day', 'hour', 'minute', 'second', 'millisecond')
    if round_period not in period_names:
        raise Exception(f'round_period "{round_period}" invalid, should be one of {",".join(period_names)}')
    period_seconds = (86400, 3600, 60, 1, 1 / pow(10, 3))
    period_desc = ('days', 'hours', 'minutes', 'seconds', 'msecs')
    round_i = period_names.index(round_period)

    string = ''
    remainder = tdelta.total_seconds()
    for i in range(len(period_names)):
        q, remainder = divmod(remainder, period_seconds[i])
        if int(q) > 0:
            if not len(string) == 0:
                string += ' '
            string += f'{q:.0f} {period_desc[i]}'
        if i == round_i:
            break
        if i == round_i + 1:
            string += f'{remainder} {period_desc[round_i]}'
            break

    return string


"""
    Authors: Conor Behard Roberts
    Description: When user is locked out add message and redirect to home page
"""


def lockout(request, credentials, *args, **kwargs):
    try:
        username = request.POST.get("username")
        ip_address = request.axes_ip_address
        account = AccessAttempt.objects.filter(username=username).filter(ip_address=ip_address)
        current_time = datetime.datetime.now()
        timeout = 5  # In minutes
        result = AccessAttempt.objects.raw(
            '''
                SELECT axes_accessattempt.id, base_accessattemptaddons.expiration_date
                FROM axes_accessattempt
                INNER JOIN base_accessattemptaddons
                ON axes_accessattempt.id = base_accessattemptaddons.accessattempt_id
                WHERE axes_accessattempt.username = %s and axes_accessattempt.ip_address = %s
                ''', [username, ip_address]
        )[0]

        # Check if the user still has to wait to login again
        if (current_time < result.expiration_date):
            time = result.expiration_date - current_time
            time_s = strfdelta_round(time)
            messages.warning(request, (f"Locked out for {time_s} due to too many login failures"))
        else:
            # Delete the user from the timeout model and re-request the login
            account.delete()
            return loginPage(request)

    except IndexError:
        expiration_date = current_time + datetime.timedelta(minutes=timeout)
        id = AccessAttempt.objects.filter(username=username, ip_address=ip_address)[0].id
        addons = AccessAttemptAddons(expiration_date=expiration_date, accessattempt_id=id)
        messages.warning(request, (f"Locked out for {timeout} minutes due to too many login failures"))
        addons.save()

    return redirect('login')


"""
    Authors: Conor Behard Roberts
    Description: When a user request to change their password the email they send is checked to see if it exists within the user database
"""


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():  # Send email if the user email exists in the database
                for user in associated_users:
                    subject = "Password Reset Required"
                    email_template = "password/password_reset_email.txt"
                    body = {
                        "email": user.email,
                        "domain": "localhost:8000",
                        "site_name": "exeter",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email = render_to_string(email_template, body)
                    try:
                        email_send = EmailMessage(subject, email, to=[user.email])
                        email_send.send()
                    except BadHeaderError:
                        return HttpResponse("invalid header found")
                    return redirect("/reset_password/done/")
        else:  # If the user email is not in the database display a message
            messages.warning(request, "Email does not exist in database")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form": password_reset_form})


"""
    Authors: Michael Hills
    Description: View to show the responses logged in user
"""


@login_required(login_url='/login')
def myResponses(request):
    responses = Responses.objects.filter(user=request.user).order_by('-created')

    categories = Category.objects.all()
    context = {'responses': responses, 'categories': categories}

    return render(request, 'base/myResponses.html', context)


"""
    Authors: Michael Hills
    Description: View to show all the responses to challenges
"""


def recentActivity(request):
    responses = Responses.objects.all().order_by('-created')
    categories = Category.objects.all()
    context = {'responses': responses, 'categories': categories}

    return render(request, 'base/recentActivity.html', context)


"""
    Authors: Michael Hills
    Description: View to show the responses of a challenge
"""


def challengeResponses(request, pk):
    challenge = Challenges.objects.get(id=pk)
    responses = Responses.objects.filter(challenge=challenge).order_by('-created')
    categories = Category.objects.all()
    context = {'responses': responses, 'challenge': challenge, 'categories': categories}
    return render(request, 'base/challengeResponses.html', context)


"""
    Authors: Michael Hills
    Description: View to show the responses of a user
"""


def userResponses(request, pk):
    user = User.objects.get(id=pk)
    responses = Responses.objects.filter(user=user).order_by('-created')
    categories = Category.objects.all()
    context = {'responses': responses, 'user': user, 'categories': categories}
    return render(request, 'base/userResponses.html', context)


"""
    Authors: Michael Hills
    Description: View to like a response to a challenge
"""


@login_required(login_url='/login')
def likeResponse(request):

    # Get the response that has been liked

    if request.method == 'POST':
        response_id = request.POST.get('response_id')
        response = Responses.objects.get(id=response_id)

        profile = response.user.profile

        # If user has already liked the response
        if request.user in response.liked.all():
            response.liked.remove(request.user)
            profile.points -= 1

        else:
            response.liked.add(request.user)
            profile.points += 1

        profile.save()

        like, created = Likes.objects.get_or_create(user=request.user, response_id=response_id)

        # Change content of button based on if it is already liked
        if not created:
            if like.value == 'like':

                like.value = 'Unlike'
            else:
                like.value = 'Like'

        like.save()
    return redirect(request.META.get('HTTP_REFERER'))


"""
    Authors: Conor Behard Roberts
    Description: Function to sign the user in with Microsoft single sign on
"""


def sign_in_sso(request):
    # Get the sign-in flow
    flow = get_sign_in_flow()
    # Save the expected flow so we can use it in the callback
    try:
        request.session['auth_flow'] = flow
    except Exception as e:
        print(e)
    # Redirect to the Azure sign-in page
    return HttpResponseRedirect(flow['auth_uri'])


"""
    Authors: Conor Behard Roberts
    Description: Function to sign the user out when having signed on with SSO
"""


def sign_out_sso(request):
    # Clear out the user and token
    remove_user_and_token(request)
    return HttpResponseRedirect(reverse('home'))


"""
    Authors: Conor Behard Roberts
    Description: Function which is called once the user is authenticated by SSO and if 
                 successful logs the user in
"""


def callback(request):
    # Make the token request
    result = get_token_from_code(request)
    if result == None:
        messages.warning(request, 'Failed login')
        return HttpResponseRedirect(reverse("login"))

    # Get the user's profile from graph_helper.py script
    user_details = get_user(result['access_token'])

    # Store user from auth_helper.py script
    store_user(request, user_details)

    first_time = False

    try:
        user = User.objects.get(email=user_details['mail'])
    except BaseException:
        first_time = True
        full_name = user_details['displayName'].split(", ")
        first_name = full_name[1]
        last_name = full_name[0]
        Profile.objects.create(
            user=User.objects.create_user(
                username=''.join(random.choice([chr(i) for i in range(ord('a'), ord('z'))]) for _ in range(10)),
                first_name=first_name,
                last_name=last_name,
                email=user_details['mail']),
            name=user_details['displayName'])
        user = User.objects.get(email=user_details['mail'])

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    # Adds the user to the user group
    group = Group.objects.get(name='user')
    user.groups.add(group)
    login(request, user)
    if (first_time):
        return HttpResponseRedirect(reverse("editProfile"))
    else:
        return HttpResponseRedirect(reverse("home"))
    
