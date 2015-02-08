from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from jam.forms import UploadFileForm
from jam.input import read_from_file
from django.conf import settings
import os
import json

from jam.models import Contact, Company, Profile, Channel, ChannelAdminNote, UserProfile, ChannelCategory
from django.http import HttpResponseRedirect

from swingtime import utils, forms
from swingtime import models as swingmodel
from dateutil import parser
from django import http
import calendar
from datetime import datetime, timedelta, time
from swingtime.models import Occurrence, Event
from itertools import chain, groupby
from django.db import models
from django.utils import timezone
from dateutil import rrule

upload_form = UploadFileForm

def contacts(request, contact_name):
	contacts = request.user.contact_set.all()
	data = request.POST
	show_contact = True
	contact_edit = False

	context = {'contacts': contacts, 'username': request.user.username, 'upload_form': upload_form, "controlled_channels": request.user.controlledChannels}

	if (data):
		edit = False
		go_home = data.get('back_home')
		if("export" in data): #if we want to output this as text file:
			#import pdb; pdb.set_trace()
			user = request.META['LOGNAME']
			path_name = "/Users/%s/Downloads/" % user
			f = open(os.path.join(path_name, "contacts.txt"), "w")
			for contact in contacts:
				f.write(str(contact) + ", " + str(contact.employer) + "\n")
			f.close()
		
		elif('save' in data):
			contact_name = data.get('contact_name')

			print "about to save contact"
			contact = request.user.contact_set.filter(name=contact_name).first()
			print "Contact name is " + contact.name 

			contact.name = data.get('name')
			contact.email=data.get('email')
			contact.phone_number=data.get('phone')
			contact.employer=data.get('employer')
			contact.notes=data.get('notes')

			contact.save()
			print "saved contact"

		elif(go_home == ("Back")):
			show_contact = False

		elif('contact_edit' in data or 'contact_name' in data):
			if('contact_edit' in data):
				contact_edit = True
				contact_name = data.get('contact_edit')
				show_contact = False
				print "edit pressed"
			else:
				contact_name = data.get('contact_name')
			contact = request.user.contact_set.get(name=contact_name)
			email_address = contact.email
			phone_number = contact.phone_number
			employer = contact.employer
			notes = contact.notes

			# check whether the employer exists as a company in the user's DB
			employer_exists = False
			if request.user.company_set.filter(name=employer).exists():
				employer_exists = True

			context = {'contact_edit': contact_edit, 'contacts': contacts, 'username': request.user.username, 'contact_email': contact.email,
			'show': show_contact, 'c_name': contact_name, 'contact_notes': contact.notes, "controlled_channels": request.user.controlledChannels,
			'phone_number': contact.phone_number, 'employer': employer, 'upload_form': upload_form, 'employer_exists': employer_exists}
		else: 
			for c in contacts:
				if c.name in data:
					c.delete()
					break
			contacts = request.user.contact_set.all()

	else:
		if contact_name != 'all':
			contact = request.user.contact_set.get(name=contact_name)
			email_address = contact.email
			phone_number = contact.phone_number
			employer = contact.employer
			notes = contact.notes

			# check whether the employer exists as a company in the user's DB
			employer_exists = False
			if request.user.company_set.filter(name=employer).exists():
				employer_exists = True

			context = {'contacts': contacts, 'username': request.user.username, 'contact_email': email_address,
			'show': show_contact, 'c_name': contact_name, 'contact_notes': notes, 'phone_number': phone_number,
			'employer': employer, 'upload_form': upload_form, 'employer_exists': employer_exists, "controlled_channels": request.user.controlledChannels}

	return render(request, 'jam/contacts/contacts.html', context)

def contacts_page(request, contact_name):
	contacts = request.user.contact_set.all()
	contact = request.user.contact_set.filter(name=contact_name).first()
	phone_number = contact.phone_number
	email_address = contact.email
	employer = contact.employer
	contact_notes = contact.notes

	context = {'contacts': contacts, 'c_name': contact_name, 'contact_notes': notes, 'phone_number': phone_number,
	'contact_email': email_address, 'employer': employer, "controlled_channels": request.user.controlledChannels}

	return render(request, 'jam/contact_page.html', context)

@login_required
def edit_contact(request, contact_name):
	form_data = request.POST

	user = User.objects.get(username=request.user.username)
	contact = request.user.contact_set.filter(name=contact_name).first()
	if form_data:
		if user and contact: 
			contact.name=form_data.get('contact_name')
			contact.email=form_data.get('email')
			contact.phone_number=form_data.get('phone')
			contact.employer=form_data.get('employer')
			contact.notes=form_data.get('notes')
			contact.save()
			redirect_link = '../../../contacts/' + contact.name
			return HttpResponseRedirect(redirect_link)

		else:
			contact = Contact(user=request.user.username,
							  name=form_data.get('contact_name'),
							  email=form_data.get('email'),
							  phone_number=form_data.get('phone'),
							  employer=form_data.get('employer'),
							  notes=form_data.get('notes')
							  )
			contact.save()
			redirect_link = '../../../contacts/' + contact.name
			return HttpResponseRedirect(redirect_link)


	context = {'contact_name': contact_name, 'notes': contact.notes, 'email': contact.email, 
	'phone_number': contact.phone_number, 'employer': contact.employer, "controlled_channels": request.user.controlledChannels}

	return render(request, 'jam/contacts/contact_page_edit.html', context)


def new_contact(request):
	form_data = request.POST
	
	# avoid adding contacts with the same name!
	contact_num = form_data.get('phone')
	print "contact num = " + contact_num

	contact_email = form_data.get('email')
	contact_name = form_data.get('name')
	print contact_name
	
	#print "contact name = " + contact_name

	''' see whether a contact with the same name already exists
			if it does, re-render the form with an appropriate error.
			if it doesn't, go ahead with business as usual, creating the company DB record
	'''
	if request.user.contact_set.filter(phone_number=contact_num).exists():
			#request.user.contact_set.get(name=contact_name)
		print "INVALID NUM!!!"
		msg = "Sorry, you've already added a contact with that number!"

		# return err response to AJAX via JSON
		response={}
		response["error"] = msg
		print "got here"
		return HttpResponseBadRequest(json.dumps(response),content_type="application/json")

	elif request.user.contact_set.filter(email=contact_email).exists():
			#request.user.contact_set.get(name=contact_name)
		print "INVALID EMAIL!!!"
		msg = "Sorry, you've already added a contact with that email!"

		# return err response to AJAX via JSON
		response={}
		response["error"] = msg
		print "got here"
		return HttpResponseBadRequest(json.dumps(response),content_type="application/json")

	else:
		print "making new contact!"

		contact_notes = form_data.get('notes')
		if contact_notes=='' :
			contact_notes=" "

		contact = Contact(name=contact_name,
						  phone_number=form_data.get('phone'),
						  email=form_data.get('email'),
						  employer=form_data.get('company'),
						  notes=contact_notes,
						  user=request.user)
		contact.save()
		context = {'username': request.user.username}

		return render(request, 'jam/index/index_landing_home.html', context)


