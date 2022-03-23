
from atexit import register
from ..models import Category, ReportComments, Responses,Comments
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

"""
    Authors: Kate Belson 
    Description: View for users to report a comment
"""
def reportAComment(request, pk):
    categories = Category.objects.all()

    comment = Comments.objects.get(id=pk)

    context = {'categories': categories, 'comment': comment}

    if request.method == "POST":

        reported = ReportComments(user=request.user,reason = request.POST.get('reason'), comment=comment)
        reported.save()
        return redirect('home')


    return render(request,'base/reportAComment.html',context)

"""
    Authors: Kate Belson 
    Description: View for game masters to accept or delete reported comments
"""
def reportedComments(request):
    reports = ReportComments.objects.all()
    categories = Category.objects.all()
    context = {'reports': reports,'categories': categories}

    if request.method == "POST":

        try:
  
            obj = request.POST.get('commentID')
            obj2 = request.POST.get('reportID')
            Comments.objects.filter(id=obj).delete()
            ReportComments.objects.filter(id=obj2).delete()

        except:
            obj2 = request.POST.get('reportID')
            ReportComments.objects.filter(id=obj2).delete()



    return render(request,'base/reportedComments.html',context)

"""
    Authors: Kate Belson 
    Description: View for being able to delete your own comments
"""
def deleteComment(request,pk):
    categories = Category.objects.all()

    context = {'categories': categories}

    if request.method == "POST":

        try:

            delete = request.POST.get('delete')
            if delete == "True":
                
                Comments.objects.filter(id=pk).delete()

            return redirect('home')

                
        except:
            return redirect('home')

    return render(request,'base/deleteComment.html',context) 