from django.contrib import admin
from .models import Profile, Category, Challenges

#adding models admins can access
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Challenges)
