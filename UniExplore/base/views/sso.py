from ..models import Profile
from ..auth_helper import get_sign_in_flow, get_token_from_code, store_user, remove_user_and_token
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from ..graph_helper import *
from django.contrib.auth.models import Group
import random

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
        messages.info(request, 'Please change your username')
        return HttpResponseRedirect(reverse("editProfile"))
    else:
        return HttpResponseRedirect(reverse("home"))
    