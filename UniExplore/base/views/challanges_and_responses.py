from email.headerregistry import Group
from ..decorators import allowed_users
from decouple import config
from ..forms import ChallengeForm, ResponseForm
from ..models import Category, Challenges, CompleteRiddle, DailyRiddle, Responses, Comments, Upgrade
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from django.forms import ModelChoiceField
from django.contrib import messages
from django.utils import timezone
import requests
import json

"""
    Authors: Michael Hills, Jack Purkiss, Kate Belson 
    Description: Only allow game masters and developers to create challenge
"""
@allowed_users(allowed_roles=["game_master", 'developer'])
def createChallenge(request):
    categories = Category.objects.all()
    form = ChallengeForm()

    if len(categories) < 3:
        photography = Category(name="Photography")
        photography.save()
        athletic = Category(name="Athletic")
        athletic.save()
        descriptive = Category(name="Descriptive")
        descriptive.save()
        categories = Category.objects.all()

    form.fields['category'] = ModelChoiceField(categories.exclude(name="Weekly"))

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
        messages.warning(request, 'ERROR: The challenge you selected has expired!')
        return redirect('home')
    
    

    if request.method == 'POST':
        form = ResponseForm(request.POST, request.FILES)
        # If valid response, add to database
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.challenge = challenge

            # analyse uploaded image
            developer_mode = False
            invalid = False
            if developer_mode == False:
                if len(request.FILES) > 0:
                    try:
                        img = request.FILES["photograph"].file.getvalue()
                        invalid = analyse_image({'media': img})
                    except Exception:
                        messages.warning(request, 'ERROR: The photo you tried to upload is not in the correct format')
                        context = {'form': form, 'categories': categories}
                        return render(request, 'base/createResponse.html', context)

            if invalid == True:
                messages.warning(request, 'ERROR: The photo you tried to upload goes against our terms of service!')
                context = {'form': form, 'categories': categories}
                return render(request, 'base/createResponse.html', context)
            else:
                obj.save()
                profile = request.user.profile
                profile.points += challenge.points
                profile.save()
                return redirect('home')

    context = {'form': form, 'categories': categories}
    return render(request, 'base/createResponse.html', context)

def analyse_image(img):
    params = { 'workflow': 'wfl_brNwJk9abjFRDu54kAc6y', 'api_user': config('image_analysis_api_user'),
                'api_secret': config('image_analysis_api_key')}

    request = requests.post('https://api.sightengine.com/1.0/check-workflow.json', files=img, data=params)
    output = json.loads(request.text)
    return output['summary']['action'] == 'reject'


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



"""
    Authors: Michael Hills
    Description: view to see daily riddle
"""
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


#MY CODE IM DOING IS HERE
"""
    Authors: Kate Belson 
    Description: View for game masters to accept or delete reported posts 
"""
def sortReported(request):
    upgrades = Upgrade.objects.all()
    categories = Category.objects.all()
    context = {'upgrades': upgrades,'categories': categories}

    if request.method == "POST":

        try:
  
            obj = request.POST.get('userID')
            obj2 = request.POST.get('upgradeID')
            toUpgrade = User.objects.get(id = obj)
            group = Group.objects.get(name='game_master')
            group.user_set.add(toUpgrade)
            Upgrade.objects.filter(id=obj2).delete()

        except:
            obj2 = request.POST.get('upgradeID')
            Upgrade.objects.filter(id=obj2).delete()



    return render(request,'base/reportedPosts.html',context)


"""
    Authors: Michael Hills
    Description: View for users to request to be upgraded to gamemaster
"""
def requestMaster(request):
    categories = Category.objects.all()
    context = {'categories': categories}

    if request.method == "POST":

        reported = Upgrade(user=request.user,reason = request.POST.get('reason'))
        reported.save()
        return redirect('home')


    return render(request,'base/reportAPost.html',context)

