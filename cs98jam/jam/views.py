from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from jam.models import Contact


# Create your views here.
@login_required
def index(request):
    context = {}
    return render(request, 'jam/index.html', context)

def profile(request):
	context = {}
	return render(request, 'jam/profile.html', context)

def new_contact(request):
	form_data = request.POST
	contact = Contact(name=form_data.get('name'), phone_number=form_data.get('phone'))
	contact.save()
	return HttpResponse()

def new_company(request):
	form_data = request.POST
	return HttpResponse()

def new_event(request):
	form_data = request.POST
	return HttpResponse()