from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django import forms
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from cs98jam.forms import *
import datetime, random, sha
from django.core.mail import send_mail
from django.contrib.auth import *
from django.http import *
from jam.models import UserProfile
from django.utils import timezone


def main_page(request):
    return render_to_response('index.html')

def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')
	
def register(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            new_user = form.save()

            # user has 5 days to activate...or else
            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_key = sha.new(salt+new_user.username).hexdigest()
            key_expires = timezone.now() + datetime.timedelta(5)
            # create user's associated user profile!
            new_profile = UserProfile(user=new_user,
                                      activation_key=activation_key,
                                      key_expires=key_expires)
            new_profile.save()

            # create a new registration profile associated with the user
            #registration = RegistrationProfile.objects.create(user = new_user)
            send_activation_email(new_user,new_profile)
            return HttpResponseRedirect("/activate/")
    else:
        form = UserSignupForm()
    return render(request, "registration/register.html", {
        'form': form,
    })
	
	

# returns standard "activation email on the way" message
def activate(request):
    return render_to_response('registration/activate.html')

# send activation email with appropriate link
def send_activation_email(user,new_profile):
    # eventually replace with real site address!!!!!!!
    site = 'http://127.0.0.1:8000'
    email_subject = 'JobApplicationManager Account Confirmation'
    activation_link =  site + '/activate/confirm/' + new_profile.activation_key

    email_body = "Howdy!\n\nYou're receiving this email since you recently signed up for a JAM account! If you're receiving this email in error, please ignore it. Otherwise, click here: " + activation_link + " to activate your account within the next 7 days!\n" 
    send_mail(email_subject, email_body, 'no-reply@gmail.com', [user.email], fail_silently =False)

# confirm that activation link's parameter matches user profile's activation key
# if confirmed, activate user's account
def confirm(request, activation_key):
    user_profile = get_object_or_404(UserProfile,
                                     activation_key=activation_key)
    if user_profile.key_expires < timezone.now():
        return render_to_response('registration/confirm_expired.html')
    user_account = user_profile.user
    user_account.is_active = True
    user_account.save()
    return render_to_response('registration/confirm_successful.html')