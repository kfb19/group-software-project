from django.urls import path
from . import views
urlpatterns = [

    path('',views.home, name="home"),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/',views.userProfile,name='profile'),
    path('create-challenge/', views.createChallenge,name='createChallenge'),
    path('create-response/<int:pk>/',views.createResponse,name='createResponse'),

]