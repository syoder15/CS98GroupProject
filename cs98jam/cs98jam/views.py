from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import HttpResponseRedirect

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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/login/")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })