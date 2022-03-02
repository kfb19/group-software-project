from django.urls import path
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views
urlpatterns = [

    path('', views.home, name="home"),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/',views.userProfile,name='profile'),
    path('create-challenge/', views.createChallenge,name='createChallenge'),
    path('create-response/<int:pk>/',views.createResponse,name='createResponse'),
    path('recent-activity/',views.recentActivity,name='recentActivity'),
    path('challenge-responses/<int:pk>',views.challengeResponses,name='challengeResponses'),
    path('userResponses/<int:pk>',views.userResponses,name='userResponses'),
    path('likes/', views.likeResponse, name='like-post'),
    path('leaderboard/',views.leaderboard,name='leaderboard'),




    # urls for password resetting
    path('reset_password/', views.password_reset_request, name='password_reset'),
    path(
        'reset_password/done/',
        PasswordResetDoneView.as_view(
            template_name='password/password_reset_done.html'),
        name='password_reset_done'),
    path(
        'reset_password/confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name="password/password_reset_confirm.html"),
        name='password_reset_confirm'),
    path(
        'reset_password/complete/',
        PasswordResetCompleteView.as_view(
            template_name='password/password_reset_complete.html'),
        name='password_reset_complete'),


    path('my-responses/', views.myResponses, name='myResponses'),

    # Urls for SSO
    path('sign-in-sso', views.sign_in_sso, name='sign-in-sso'),
    path('sign-out-sso', views.sign_out_sso, name='sign-out-sso'),
    path('callback', views.callback, name='callback'),

]
