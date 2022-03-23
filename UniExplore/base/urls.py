from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

"""
Authors: 
    - Michael Hills
    - Conor Behard Roberts
    - Tomas Premoli
    - Lucas Smith
    - Kate Belson 
"""

from django.urls import path
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from . import views

urlpatterns = [

    # Author: Michael Hills, Lucas Smith, Kate Belson 
    path('', views.home, name="home"),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('create-challenge/', views.createChallenge, name='createChallenge'),
    path('create-response/<int:pk>/', views.createResponse, name='createResponse'),
    path('recent-activity/', views.recentActivity, name='recentActivity'),
    path('challenge-responses/<int:pk>', views.challengeResponses, name='challengeResponses'),
    path('userResponses/<int:pk>', views.userResponses, name='userResponses'),
    path('create-challenge/', views.createChallenge, name='createChallenge'),
    path('create-response/<int:pk>/', views.createResponse, name='createResponse'),
    path('challenge-responses/<int:pk>', views.challengeResponses, name='challengeResponses'),
    path('userResponses/<int:pk>', views.userResponses, name='userResponses'),
    path('likes/', views.likeResponse, name='like-post'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('my-responses/', views.myResponses, name='myResponses'),
    path('createComment/<int:pk>', views.createComment, name='createComments'),
    path('viewComments/<int:pk>', views.viewComments, name='viewComments'),
    path('viewRiddle/<int:pk>', views.viewRiddle, name='viewRiddle'),
    path('deleteProfile/',views.deleteProfile, name='deleteProfile'),
    path('upgradeUser/', views.upgradeUser, name ='upgradeUser' ),
    path('requestMaster/', views.requestMaster,name='requestMaster'),
    path('reportAPost/<int:pk>', views.reportAPost, name ='reportAPost' ),
    path('reportedPosts/', views.reportedPosts,name='reportedPosts'),
    path('deletePost/<int:pk>/', views.deletePost,name='deletePost'),
    path('reportAComment/<int:pk>', views.reportAComment, name ='reportAComment' ),
    path('reportedComments/', views.reportedComments,name='reportedComments'),
    path('deleteComment/<int:pk>/', views.deleteComment,name='deleteComment'),

    # Author: Lucas Smith
    path('profile_edit/', views.editProfile, name='editProfile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('follow/<str:username>/', views.followUser, name='followUser'),
    path('recentFollowerActivity/', views.recentFollowerActivity, name='recentFollowerActivity'),

    # Author: Tomas Premoli
    path('profile/', views.userProfile, name='profile'),

    # Author: Conor Behard Roberts
    # Description: urls for password resetting
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

    # Author: Conor Behard Roberts
    # Description: urls for SSO
    path('sign-in-sso', views.sign_in_sso, name='sign-in-sso'),
    path('sign-out-sso', views.sign_out_sso, name='sign-out-sso'),
    path('callback', views.callback, name='callback'),

    # URL for email verification
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    
    # URLS for GDPR
    path('terms-of-service/', views.tos, name='ToS'),
    path('cookies/', views.cookie, name='cookie'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
]

# Need to change this before final deployment as django recommends to do this another way
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
