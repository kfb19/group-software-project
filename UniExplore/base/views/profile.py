from django.http import Http404, HttpResponseRedirect
from pytz import timezone
from ..models import Category, Responses, Comments, Upgrade, Profile
from ..forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import io
import requests
import json
from decouple import config

"""
    Authors: Lucas Smith,
    Description: Redirects to the currently authenticated user's profile
"""


@login_required(login_url='/login')
def userProfile(request):
    return HttpResponseRedirect("/profile/" + request.user.username)

"""
    Authors: Lucas Smith, Michael Hills
    Description: View another user's (or your own) profile from parameter in URl specified
"""


def profile(request, username):
    # If username doesn't exist, 404 error
    try:
        usertofetch = User.objects.get(username=username)
    except:
        messages.error("User not found")
        return HttpResponseRedirect("/")

    # Handling whether edit profile options should show
    editable = False
    if request.user == usertofetch:
        editable = True

    responses = Responses.objects.filter(user=usertofetch).order_by('-created')
    comments = Comments.objects.all().order_by('-date_added')

    game_master = False
    if request.user.groups.filter(name='game_master').exists():
        game_master = True

    following = False

    user_profile = Profile.objects.get(user=request.user)
    follow_profile = Profile.objects.get(user=usertofetch)

    if user_profile.following.filter(user_id=follow_profile.user_id).exists():
        following = True

    print(following)

    categories = Category.objects.all()
    context = {
        'responses': responses,
        'categories': categories,
        'comments': comments,
        'game_master': game_master,
        'editable': editable,
        'user': usertofetch,
        'following': following
    }

    return render(request, 'base/profile.html', context)


"""
    Authors: Lucas Smith
    Description: Added functionality to follow/unfollow users
"""

def followUser(request, username):
    user_profile = Profile.objects.get(user=request.user)
    follow_user = User.objects.get(username=username)
    follow_profile = Profile.objects.get(user=follow_user)

    if user_profile.following.filter(user_id=follow_profile.user_id).exists():
        user_profile.following.remove(follow_profile)
    else:
        user_profile.following.add(follow_profile)

    user_profile.save()

    return HttpResponseRedirect("/profile/"+username)


"""
    Authors: Michael Hills
    Description: View for game masters to accept user requests to be a gamemaster
"""
@login_required(login_url='/login')
def upgradeUser(request):
    upgrades = Upgrade.objects.all()
    categories = Category.objects.all()
    context = {'upgrades': upgrades, 'categories': categories}

    if request.method == "POST":

        try:

            obj = request.POST.get('userID')
            obj2 = request.POST.get('upgradeID')
            toUpgrade = User.objects.get(id=obj)
            group = Group.objects.get(name='game_master')
            group.user_set.add(toUpgrade)
            Upgrade.objects.filter(id=obj2).delete()

        except:
            obj2 = request.POST.get('upgradeID')
            Upgrade.objects.filter(id=obj2).delete()

    return render(request, 'base/upgradeUser.html', context)


"""
    Authors: Michael Hills
    Description: View for users to request to be upgraded to gamemaster
"""
@login_required(login_url='/login')
def requestMaster(request):
    categories = Category.objects.all()
    context = {'categories': categories}

    if request.method == "POST":
        master = Upgrade(user=request.user, reason=request.POST.get('reason'))
        master.save()
        return redirect('home')

    return render(request, 'base/requestMaster.html', context)


"""
    Authors: Michael Hills
    Description: View for users to delete their account
"""


@login_required(login_url='/login')
def deleteProfile(request):
    if request.method == 'POST':
        User.objects.filter(id=request.user.id).delete()
        messages.success(request, 'Account Successfully Deleted')
        return redirect("login")

    return render(request, 'base/deleteProfile.html')


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

            # Analyse image uploaded
            developer_mode = False
            invalid = False
            if developer_mode == False:
                if len(request.FILES) > 0:
                    try:
                        if isinstance(request.FILES["picture"].file, io.BytesIO):
                            img = request.FILES["picture"].file.getvalue()
                            invalid = analyse_image({'media': img})
                        else:
                            img = request.FILES["picture"].file.file.read()
                            invalid = analyse_image({'media': img})
                    except Exception as e:
                        messages.warning(request, 'ERROR: The photo you tried to upload is not in the correct format')
                        context = {'user_form': user_form, 'profile_form': profile_form}
                        return render(request, 'base/profile_edit.html', context)

            if invalid:
                messages.warning(request, 'ERROR: The photo you tried to upload goes against our terms of service!')
                return redirect('editProfile')
            else:
                try:
                    if request.user.username != username:
                        User.objects.get(username=username)
                    else:
                        raise BaseException()
                except BaseException:
                    user_form.save()
                    profile_form.save()
                    messages.success(request, f'Your account has been updated successfully.')
                    return redirect('profile')

                messages.warning(request, "This username already exists")
                return redirect('editProfile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'base/profile_edit.html', context)


def analyse_image(img):
    params = {'workflow': 'wfl_brNwJk9abjFRDu54kAc6y', 'api_user': config('image_analysis_api_user'),
              'api_secret': config('image_analysis_api_key')}

    request = requests.post('https://api.sightengine.com/1.0/check-workflow.json', files=img, data=params)
    output = json.loads(request.text)
    return output['summary']['action'] == 'reject'
