from email.headerregistry import Group
from ..models import Category, Challenges, CompleteRiddle, Responses, DailyRiddle
from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import Group as Groups
from django.forms import ValidationError
import json
from random import choice
"""
    Authors: Michael Hills, Tomas Premoli
    Description: View for the main homepage
"""
def home(request):

    # Checks if there's a valid current riddle and generates it if not
    current = DailyRiddle.objects.all()
    for riddle in current:
        if riddle.created.day != timezone.now().day:
            DailyRiddle.objects.filter(id=riddle.id).delete()
            generateDailyRiddle()

    if len(current) == 0:
        generateDailyRiddle()

    
    categories = Category.objects.all()

    unexpired_challenges = Challenges.objects.all()

    # If no weekly challenges, generate one
    if (len(
            unexpired_challenges
            .exclude(Q(is_weekly_challenge=False))
            .filter(Q(expires_on__gt=timezone.now()))
            ) == 0):
        print("No weekly challenges! Generating...")
        generate_weekly_challenges(request)

    # Checks if groups exists and if not create them
    Groups.objects.get_or_create(name="user")
    Groups.objects.get_or_create(name="game-master")

    # Get the filter from the ?q= in the URL
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    # Get all challenges, not done by the current user
    if request.user.is_authenticated:
        Completed_Riddles = CompleteRiddle.objects.filter(user=request.user).values_list('riddle_id')
        daily_riddle = DailyRiddle.objects.exclude(id__in=Completed_Riddles).first()
        print(daily_riddle)
        responses = Responses.objects.filter(user=request.user).values_list('challenge_id')

        challenges = Challenges.objects.exclude(id__in=responses).filter(
            Q(category__name__icontains=q),
            Q(expires_on__gt=timezone.now()) # This makes sure expired aren't rendered
            ).order_by('-created')

        
    else:
        challenges = Challenges.objects.filter(
            Q(category__name__icontains=q), 
            Q(expires_on__gt=timezone.now()) # This makes sure expired aren't rendered
            ).order_by('-created')

        daily_riddle = DailyRiddle.objects.all().first()
        # add locations to map

        # Variables to pass to the database
        

    context = {'categories': categories, 'challenges': challenges,'dailyRiddle':daily_riddle}

    return render(request, 'base/home.html', context)

def generate_weekly_challenges(request):
    # loads locations and default challenges
    challenge_json = json.load(open('base/resources/default_challenges.json'))
    location_json = json.load(open('base/resources/sample_locations.json'))

    weekly_category = Category.objects.filter(Q(name="Weekly")).first()

    expiry_date = timezone.now() + timezone.timedelta(days=7)

    # If no weekly category, create it.
    if(weekly_category == None):
        new_challenge = Category(name="Weekly")
        new_challenge.save()
        weekly_category = Category.objects.filter(Q(name="Weekly")).first()

    for i in range(5):
        # Select random challenge and location
        selected_challenge = choice(challenge_json)
        selected_location = choice(location_json)

        # Generate challenge with that info and upload to challenges
        new_challenge = Challenges(
            name = selected_location['name'],
            category = weekly_category,
            points = selected_challenge['points'],
            description = (selected_challenge['name'] + " "  +selected_challenge['description']),
            expires_on = expiry_date,
            is_weekly_challenge = True,
            lat = selected_location['lat'],
            long = selected_location['long']
        )

        new_challenge.save()


def generateDailyRiddle():
    # Loads random riddle and saves into database
    riddle_json = json.load(open('base/resources/daily_riddles.json'))
    
    selected_riddle = choice(riddle_json)
    new_riddle = DailyRiddle(
        name = selected_riddle['description'],
        points = selected_riddle['points'],
        lat = selected_riddle['lat'],
        long = selected_riddle['long'],
        answer = selected_riddle['answer']
    )
    new_riddle.save()
    

    
     