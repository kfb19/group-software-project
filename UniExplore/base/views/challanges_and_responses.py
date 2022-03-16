from ..decorators import allowed_users
from ..forms import ChallengeForm, ResponseForm
from ..models import Category, Challenges, CompleteRiddle, DailyRiddle, Responses, Comments
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from django.forms import ModelChoiceField
from django.contrib import messages
from django.utils import timezone

"""
    Authors: Michael Hills, Jack Purkiss
    Description: Only allow game masters and developers to create challenge
"""
@allowed_users(allowed_roles=["game_master", 'developer'])
def createChallenge(request):
    categories = Category.objects.all()
    form = ChallengeForm()

    form.fields['category'] = ModelChoiceField(Category.objects.all().exclude(name="Weekly"))

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
    Authors: Michael Hills, Kate Belson, Tomas Premoli
    Description: View to complete a challenge 
"""
@login_required(login_url='/login')
def createResponse(request, pk):
    challenge = Challenges.objects.get(id=pk)
    categories = Category.objects.all()
    form = ResponseForm()

    # This prevents from a user uploading multiple responses to challenges
    existing_responses = Responses.objects.filter(
            Q(challenge=challenge),
            Q(user=request.user)).order_by('-created')
    
    # If it's been completed by said user, throw an error
    if len(existing_responses) != 0:
        messages.warning(request, 'ERROR: Can only respond to a challenge once!')
        return redirect('home')
    # If it's expired, throw an error
    elif challenge.expires_on < timezone.now():
        print("ruh oh")
        messages.warning(request, 'ERROR: The challenge you selected to has expired!')
        return redirect('home')


    if request.method == 'POST':
        form = ResponseForm(request.POST, request.FILES)

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
    comments = Comments.objects.all().order_by('-date_added')
    responses = Responses.objects.filter(challenge=challenge).order_by('-created')
    categories = Category.objects.all()
    context = {'responses': responses, 'challenge': challenge, 'categories': categories, 'comments':comments}
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


@login_required(login_url='/login')
def viewRiddle(request,pk):
    dailyRiddle = DailyRiddle.objects.get(id=pk)
    categories = Category.objects.all()
    

    completed = CompleteRiddle.objects.filter(riddle=dailyRiddle)
    allowed = True
    
    if len(completed) > 0:
        allowed = False

    else:

        complete = CompleteRiddle(riddle=dailyRiddle,user=request.user)
        complete.save()
        profile = request.user.profile
        profile.points += dailyRiddle.points

        profile.save()
        complete.save()

    context = {'dailyRiddle':dailyRiddle, 'categories':categories,'allowed': allowed}

    
    
    return render(request,'base/viewRiddle.html', context)

