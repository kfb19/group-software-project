from ..models import Category, Responses
from django.shortcuts import render

"""
    Authors: Michael Hills
    Description: View to show all the responses to challenges
"""


def recentActivity(request):
    responses = Responses.objects.all().order_by('-created')
    categories = Category.objects.all()
    context = {'responses': responses, 'categories': categories}

    return render(request, 'base/recentActivity.html', context)