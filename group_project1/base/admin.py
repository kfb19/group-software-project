from django.contrib import admin
from .models import Profile, Category, Challenges,Responses

# Adding models admins can access
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Challenges)
admin.site.register(Responses)
