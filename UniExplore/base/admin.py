"""
Authors: 
    - Michael Hills
"""

from django.contrib import admin
from .models import CompleteRiddle, DailyRiddle, Profile, Category, Challenges, Responses, Likes, Comments

# Adding models admins can access (Michael Hills)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Challenges)
admin.site.register(Responses)
admin.site.register(Likes)
admin.site.register(Comments)
admin.site.register(DailyRiddle)
admin.site.register(CompleteRiddle)