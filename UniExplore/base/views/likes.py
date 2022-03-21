from django.http import JsonResponse
from ..models import Likes, Responses
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

"""
    Authors: Michael Hills
    Description: View to like a response to a challenge
"""
@login_required(login_url='/login')
def likeResponse(request):


    # Get the response that has been liked

    if request.method == 'POST':

        response_id = request.body.decode('utf-8')
       
        response = Responses.objects.get(id=response_id)

        profile = response.user.profile

        # If user has already liked the response
        if request.user in response.liked.all():
            response.liked.remove(request.user)
            profile.points -= 1

        else:
            response.liked.add(request.user)
            profile.points += 1

        profile.save()

        like, created = Likes.objects.get_or_create(user=request.user, response_id=response_id)

        # Change content of button based on if it is already liked
        if not created:
            if like.value == 'like':

                like.value = 'Unlike'
            else:
                like.value = 'Like'


        like.save()

    return JsonResponse({})
        
       
        

   