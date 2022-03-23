from atexit import register
from ..models import Category, Responses, Comments
from django.shortcuts import render
from django.contrib.auth.decorators import login_required



"""
    Authors: Michael Hills
    Description: View to show all the responses to challenges
"""
@login_required(login_url='/login')
def recentActivity(request):
    
    responses = Responses.objects.all().order_by('-created')
    categories = Category.objects.all()
    comments = Comments.objects.all().order_by('-date_added')
    
    
    context = {'responses': responses, 'categories': categories, 'comments':comments}

    return render(request, 'base/recentActivity.html', context)


"""
    Authors: Lucas Smith
    Description: View to show responses to challenges from people the user follows
"""
def recentFollowerActivity(request):
    users_followed = request.user.profile.following.all()

    responses = Responses.objects.filter(user__profile__in=users_followed).order_by('-created')

    categories = Category.objects.all()
    comments = Comments.objects.all().order_by('-date_added')

    context = {'responses': responses, 'categories': categories, 'comments': comments}

    return render(request, 'base/recentActivity.html', context)



