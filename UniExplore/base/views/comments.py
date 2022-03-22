
from atexit import register
from ..models import Responses,Comments
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .. forms import commentForm
from better_profanity import profanity

"""
    Authors: Michael Hills
    Description: View to create a comment
"""
@login_required(login_url='/login')
def createComment(request, pk):

    
    response = Responses.objects.get(id=pk)

    if request.method == 'POST':
        form = commentForm(request.POST)
        # If valid response, add to database
        if form.is_valid():
            profanity.load_censor_words()
            obj = form.save(commit=False)
            obj.user = request.user
            obj.response = response
            obj.text = profanity.censor(obj.text)
            obj.save()
            return redirect('home')

            
    form = commentForm()
    
    context = {'response': response, 'form':form}
    return render(request, 'base/createComments.html', context)


"""
    Authors: Michael Hills
    Description: View to see all comments on a response
"""
@login_required(login_url='/login')
def viewComments(request, pk):

    
    response = Responses.objects.get(id=pk)
    comments = Comments.objects.all().filter(response=response).order_by('-date_added')

    
    context = {'response': response,'comments': comments}
    return render(request, 'base/viewComments.html', context)

