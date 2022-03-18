from ..forms import UserRegisterForm
from ..models import Profile
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import Group
from ..tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_str
from django.conf import settings

"""
    Authors: Conor Behard Roberts
    Description: Checks to see if an email is valid given a valid suffix
"""
def is_valid_email(email, valid_suffix):
    ending = email.split('@')[1].lower()
    return valid_suffix.lower() == ending


"""
    Authors: Michael Hills, Conor Behard Roberts
    Description: Function for user registration
"""
def registerPage(request):

    # Getting form from forms.py
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        # Save form if it is valid
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username').lower().capitalize()

            try:
                User.objects.get(username=username)
            except BaseException:
                if is_valid_email(email, settings.EMAIL_EXTENSION):
                    try:
                        # Check to see if there is already a user with the same email registered
                        User.objects.get(email=email)
                    except BaseException:
                        user = form.save(commit=False)
                        user.is_active = False
                        user.save()

                        if settings.DEBUG == False:
                            subject = 'Activate Your UniExplore Account'
                            message = render_to_string('email_verification/account_activation_email.html', {
                                'user': user,
                                'domain': 'localhost:8000',
                                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                'token': account_activation_token.make_token(user),
                            })
                            user.email_user(subject, message)
                            messages.success(request, ('Please Confirm your email to complete registration.'))

                        user.backend = 'django.contrib.auth.backends.ModelBackend'  # Sets the backend authentication model

                        Profile.objects.create(
                            user=user,
                            name=username,
                        )
                        # Adds the user to the user group
                        group = Group.objects.get(name='user')
                        user.groups.add(group)

                        if settings.DEBUG == True:
                            login(request, user)
                            messages.success(request, f'Account created for {username}!')
                            return redirect('home')
                            
                        return redirect('login')

                    messages.warning(request, "A User with this email already exists")
                    return redirect('register')
                else:
                    messages.warning(request, "Must sign up with an email ending in exeter.ac.uk")
                    return redirect('register')
            messages.warning(request, "This username is taken")
            return redirect('register')
    context = {'form': form}
    return render(request, 'base/login_register.html', context)


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.backend = 'django.contrib.auth.backends.ModelBackend'  # Sets the backend authenticaion model
       
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()

        login(request, user)
        messages.success(request, ('Your account has been confirmed.'))
        return redirect('home')
    else:
        messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
        return redirect('home')
