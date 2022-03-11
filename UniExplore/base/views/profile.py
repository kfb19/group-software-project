from ..models import Category, Responses
from ..forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

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