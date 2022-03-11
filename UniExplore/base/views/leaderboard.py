from ..models import Category, Profile
from django.shortcuts import render
"""
    Authors: Michael Hills
    Description: View of the leaderboard
"""


def leaderboard(request):

    categories = Category.objects.all()
    profiles = Profile.objects.all().order_by('-points')
    context = {'profiles': profiles, 'categories': categories}
    return render(request, 'base/leaderboard.html', context)