from django.shortcuts import render


def tos(request):
    return render(request, 'GDPR/ToS.html')

def cookie(request):
    return render(request, 'GDPR/cookie.html')

def privacy_policy(request):
    return render(request, 'GDPR/privacyPolicy.html')