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
            # create a new registration profile associated with the user
            #registration = RegistrationProfile.objects.create(user = new_user)
            send_activation_email(new_user)
            return HttpResponseRedirect("/login/")
    else:
        form = UserSignupForm()
    return render(request, "registration/register.html", {
        'form': form,
    })

def send_activation_email(user):
    activation_key = 1234
    expiration_days = settings.ACCOUNT_ACTIVATION_DAYS
    site = 'http://127.0.0.1:8000'
    email_subject = 'JobApplicationManager Account Confirmation'
    activation_link =  site + '/activate/key=' + str(activation_key)

    email_body = "Howdy!\n\nYou're receiving this email since you recently signed up for a JAM account! If you're receiving this email in error, please ignore it. Otherwise, click here: " + activation_link + " to activate your account within the next 7 days!\n" 
    send_mail(email_subject, email_body, 'no-reply@gmail.com', [user.email], fail_silently =False)

def activate(request):
    activation_key = 1234567
    #activation_key = request.GET.get('key', None)
    if activation_key == None:
        raise Http404
    try:
        #user = User.objects.get(registration__uuid=activation_key)
        #user.is_active = True
        #user.save()
        #user.registration.delete()
        return HttpResponseRedirect("/login")
    except:
        raise Http404
'''
def confirm(request, activation_key):
    if request_user.is_authenticated():
        return render_to_response('confirm.html', {'has_account': True})
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
    if user_profile.key_expires < datetime.datetime.today():
            return render_to_response('confirm.html', {'expired': True})
    user_account = user_profile.user
    user_account.is_active = True
    user_account.save()
    return render_to_response('confirm.html', {'success': True})
'''