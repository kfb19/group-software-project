from ..decorators import allowed_users
from ..forms import ChallengeForm, ResponseForm
from ..models import Category, Challenges, Responses
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

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
    Description: View to show the responses of a user
"""
def userResponses(request, pk):
    user = User.objects.get(id=pk)
    responses = Responses.objects.filter(user=user).order_by('-created')
    categories = Category.objects.all()
    context = {'responses': responses, 'user': user, 'categories': categories}
    return render(request, 'base/userResponses.html', context)