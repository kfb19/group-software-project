from atexit import register
from ..models import Category, Responses, Comments
from django.shortcuts import render



"""
    Authors: Michael Hills
    Description: View to show all the responses to challenges
"""
def recentActivity(request):
    
    responses = Responses.objects.all().order_by('-created')
    categories = Category.objects.all()
    comments = Comments.objects.all().order_by('-date_added')
    
    context = {'responses': responses, 'categories': categories, 'comments':comments}

    return render(request, 'base/recentActivity.html', context)


