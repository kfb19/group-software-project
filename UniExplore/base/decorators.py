"""
Authors: 
    - Jack Purkiss
"""

from django.http import HttpResponse
from django.shortcuts import redirect

#Restricts which users can access a certain view
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
                       
            #check if user is in an allowed group
            for role in request.user.groups.all():
                group = None
                if request.user.groups.exists():
                    group = role.name
                if group in allowed_roles:
                    #allow access if they are allowed
                    return view_func(request, *args, **kwargs)
            
            #return message if they are not allowed
            return HttpResponse("You are not authorized to view this page")
        return wrapper_func
    return decorator