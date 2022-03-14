from ..models import Category, Challenges, Responses
from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone
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

        challenges = Challenges.objects.exclude(id__in=responses).filter(
            Q(category__name__icontains=q),
            Q(expires_on__gt=timezone.now()) # This makes sure expired aren'trendered
            ).order_by('-created')
    else:
        challenges = Challenges.objects.filter(
            Q(category__name__icontains=q), 
            Q(expires_on__gt=timezone.now()) # This makes sure expired aren'trendered
            ).order_by('-created')
        # add locations to map

        # Variables to pass to the database
    context = {'categories': categories, 'challenges': challenges}

    return render(request, 'base/home.html', context)