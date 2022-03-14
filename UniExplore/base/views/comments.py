
from ..models import Responses,Comments
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

"""
    Authors: Michael Hills
    Description: View to show all comments to a response
"""
def comments(request, pk):
    response = Responses.objects.get(id=pk)
    comments = Comments.objects.filter(response=response).order_by('-created')
    
    context = {'responses': response, 'comments': comments}
    return render(request, 'base/comments.html', context)