
from ..models import Responses,Comments
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .. forms import commentForm

"""
    Authors: Michael Hills
    Description: View to create a comment
"""
def createComment(request, pk):

    
    response = Responses.objects.get(id=pk)

    if request.method == 'POST':
        form = commentForm(request.POST)
        # If valid response, add to database
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.response = response
            obj.save()
            return redirect('home')

            
    form = commentForm()
    
    context = {'response': response, 'form':form}
    return render(request, 'base/createComments.html', context)