from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from jam.models import Contact, Company, Event, Profile


# Create your views here.
@login_required
def index(request):
    context = {}
    return render(request, 'jam/index.html', context)

def profile(request):
	context = {}
	form_data = request.POST
	if form_data:
		profile = Profile(first_name=form_data.get('first_name'),
						  last_name=form_data.get('last_name'),
						  email=form_data.get('email'),
						  phone_number=form_data.get('phone'),
						  address=form_data.get('address'),
						  city=form_data.get('city'),
						  state=form_data.get('state'),
						  zip_code=form_data.get('zip_code'))
		profile.save()
	return render(request, 'jam/profile.html', context)

def new_contact(request):
	form_data = request.POST
	contact = Contact(name=form_data.get('name'),
					  phone_number=form_data.get('phone'))
	contact.save()
	return HttpResponse()

def new_company(request):
	form_data = request.POST
	company = Company(name=form_data.get('name'))
	company.save()
	return HttpResponse()

def new_event(request):
	form_data = request.POST
	event = Event(name=form_data.get('name'),
					  date=form_data.get('date'))
	event.save()
	return HttpResponse()

def new_profile(request):
	import pdb; pdb.set_trace()
	form_data = request.POST
	profile = Profile(first_name=form_data.get('first name'),
					  last_name=form_data.get('last name'),
					  email=form_data.get('email'),
					  phone_number=form_data.get('phone'),
					  address=form_data.get('address'),
					  city=form_data.get('city'),
					  state=form_data.get('state'),
					  zip_code=form_data.get('zip code'))
	profile.save()
	return HttpResponse()

def companies(request):
	context = {}
	return render(request, 'jam/companies.html', context)

