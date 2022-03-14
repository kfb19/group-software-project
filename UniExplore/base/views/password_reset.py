from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

"""
    Authors: Conor Behard Roberts
    Description: When a user request to change their password the email they send is checked to see if it exists within the user database
"""
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():  # Send email if the user email exists in the database
                for user in associated_users:
                    subject = "Password Reset Required"
                    email_template = "password/password_reset_email.txt"
                    body = {
                        "email": user.email,
                        "domain": "localhost:8000",
                        "site_name": "exeter",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email = render_to_string(email_template, body)
                    try:
                        email_send = EmailMessage(subject, email, to=[user.email])
                        email_send.send()
                    except BadHeaderError:
                        return HttpResponse("invalid header found")
                    return redirect("/reset_password/done/")
        else:  # If the user email is not in the database display a message
            messages.warning(request, "Email does not exist in database")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form": password_reset_form})
