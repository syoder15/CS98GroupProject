from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from jam.forms import UploadFileForm
#from jam.input import read_from_file
from django.conf import settings
import os
import json

from jam.models import Contact, Company, Profile, Channel, ChannelAdminNote, UserProfile, ChannelCategory, Event as jam_event
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
from django.views.decorators.csrf import csrf_exempt


upload_form = UploadFileForm

@login_required
def new_company(request):
	print "in new company"
	#START OF CODE
	if request.method == "POST" and request.FILES:
		print "in new company upload multiple"
		form = UploadFileForm(request.FILES)
		read_from_file(request.user, request.FILES['filep'])
		context = {'username': request.user.username}

		#return render(request, 'jam/companies/companies.html', context)
		return companies(request,'all')
	elif request.method == "POST":
		form_data = request.POST

		# check whether we've got a valid date. if invalid, we need them to fix their form errors!
		application_deadline = form_data.get('deadline')
		validity = is_valid_date(application_deadline)
		if(validity!=''):
			# return bad request if the deadline is still invalid somehow (but very unlikely!)
			response={}
			response["error"] = validity
			print "got here"
			return HttpResponseBadRequest(json.dumps(response),content_type="application/json")

			#probs should get rid of this shit bc its dead code but yolo...soon!
			context = { 'validity' : validity }
			return render(request, 'jam/modals/modal_add_company.html', context)
		
		company_name = form_data.get('name')

		
		''' see whether a company with the same name already exists
			if it does, re-render the form with an appropriate error.
			if it doesn't, go ahead with business as usual, creating the company DB record
		'''
		if request.user.company_set.filter(name=company_name).exists():
			#request.user.company_set.get(name=company_name)
			msg = "I'm sorry, you've already added that company. Please add a different one!"

			response={}
			response["error"] = msg
			print "got here"
			return HttpResponseBadRequest(json.dumps(response),content_type="application/json")
		else: 
			'''company = Company(name=company_name,
						  application_deadline=form_data.get('deadline'),
						  notes=form_data.get('company_notes'),
						  user=request.user)
			'''
			
			#event_types = swingmodel.EventType.objects.filter(abbr='due', label='Application Deadline')
			
			#if len(event_types) == 0:
			#	swingmodel.EventType.objects.create(abbr='due', label='Application Deadline')
			#	swingmodel.EventType.objects.filter(abbr='due', label='Application Deadline')
			if (application_deadline != "" and len(application_deadline) != 0):
				year = int(application_deadline[0:4])
				month = int(application_deadline[5:7])
				day = int(application_deadline[8:10])

				title = str(company_name) + ' Deadline'
			
				evt = jam_event(
					name=title,
					event_type='Application Deadline',
					description='',
					companies=company_name,
					start_time='12:00',
					end_time='13:00',
					event_date=application_deadline,
					creator=request.user
				)
				evt.save()

				request.user.events.add(evt)
			if application_deadline == '':
				company = Company(name=company_name,notes=form_data.get('company_notes'),user=request.user, link=form_data.get('app_link'))
			else:
				company = Company(name=company_name,application_deadline=application_deadline,notes=form_data.get('company_notes'),user=request.user, link=form_data.get('app_link'))

			company.save()

			if (application_deadline != "" and len(application_deadline) != 0):
				company.events.add(evt)
			print 'made company'
			context = {'username': request.user.username}



			return render(request, 'jam/index/index_landing_home.html', context)

@login_required
@csrf_exempt
def company_page(request, company_name):
	print 'company_page view'
	companies = request.user.company_set.all()
	company = request.user.company_set.filter(name=company_name).first()
	contacts = Contact.objects.filter(user=request.user, employer=company_name)
	events = request.user.events.all()
	application_deadline = company.application_deadline
	company_notes = company.notes
	link = company.link
	has_link = False
	if link != '':
		has_link = True
	

	site = settings.DOMAIN

	app_deadline = str(application_deadline)
	datetime.strptime(app_deadline, "%Y-%m-%d")

	print 'app_deadline'
	print app_deadline

	context = {'company': companies, 'contacts': contacts,'status': company.application_status,'has_link': has_link, 'link': link, 
	'events': events, 'company_name': company_name, 'application_deadline': app_deadline, 
	'company_notes': company_notes, 'site': site, "controlled_channels": request.user.controlledChannels}
	
	return render(request, 'jam/companies/company_page.html', context)

@login_required
def edit_company(request, company_name):
	print 'edit company view'
	form_data = request.POST

	user = User.objects.get(username=request.user.username)
	company = request.user.company_set.filter(name=company_name).first()

	if form_data:
		print "GOT HERE YAY"
		if user and company: 
			company.name=form_data.get('company_name')
			company.application_deadline=form_data.get('app_deadline')
			company.notes=form_data.get('notes')
			print company.name + company.application_deadline + company.notes
			company.save()
			redirect_link = '../../../companies/' + company.name
			return HttpResponseRedirect(redirect_link)

		else:
			company = Company(user=request.user.username,
							  company_name=form_data.get('company_name'),
							  application_deadline=form_data.get('app_deadline'),
							  notes=form_data.get('notes')
							  )
			company.save()
			redirect_link = '../../../companies/' + company.name
			return HttpResponseRedirect(redirect_link)

	app_deadline = company.application_deadline
	app_deadline = str(app_deadline)
	datetime.strptime(app_deadline, "%Y-%m-%d")

	print 'app_deadline'
	print app_deadline

	context = {'company_name': company_name, 'application_deadline': app_deadline, 'notes': company.notes, "controlled_channels": request.user.controlledChannels}

	return render(request, 'jam/companies/company_page_edit.html', context)

@login_required
@csrf_exempt
def companies(request, company_name):
	print 'companies view'
	companies = request.user.company_set.all()
	companies = sorted(companies, key=lambda company: company.name)
	data = request.POST
	show_company = True
	user = User.objects.get(username = request.user.username)

	

	context = {'companies': companies, 'username': request.user.username, 'upload_form': upload_form, "controlled_channels": request.user.controlledChannels}

	if(data):
		company_edit = False
		app_deadline = ''
		
		#import pdb;pdb.set_trace()
		go_home = data.get('back_home')

		if("export" in data):
			print "got to export"
			user = request.META['LOGNAME']
			path_name = "/Users/%s/Downloads/" % user
			f = open(os.path.join(path_name, "jam_companies.txt"), "w")
			for company in companies:
				f.write(str(company) + ", " + str(company.application_deadline) + "\n")
			f.close() 

		elif('save' in data):
			company_name = data.get('name')
			company = request.user.company_set.filter(name=company_name).first()

		
			company.name = company_name
			company.application_deadline=data.get('application_deadline')
			company.notes=data.get('notes')
			company.link = data.get('app_link')
			company.save()
			


		elif('delete' in data):
			company_name = data.get('delete')
			event_title = str(company_name) + ' Deadline'
			company = request.user.company_set.filter(name=company_name)
			company.delete()
			
			event = request.user.events.filter(name=event_title)
			owned_event = request.user.owned_events.filter(name=event_title)
			event.delete()
			owned_event.delete()
			


		elif(go_home == ("Back")):
			show_company = False
		elif('company_update' in data):
			
			#c_name = data.get('app_status')
			if ('company_edit' in data): 
				company_edit = True 
				show_company = False 
			company_list = data.getlist('app_status[]')
			
			for company in companies: 
				if company.name in company_list: 
					company = request.user.company_set.get(name=company.name)
					company.application_status = True
					company.save()
				else:
					company.application_status = False
					company.save()
			companies = request.user.company_set.all()
			context = {'companies': companies, 'username': request.user.username, 'upload_form': upload_form, "controlled_channels": request.user.controlledChannels}
		elif('company_name' in data or 'company_edit' in data):
			if('company_edit' in data): 
				company_edit = True 
				show_company = False
				c_name = data.get('company_edit')
				company = request.user.company_set.get(name=c_name)
				if company.application_deadline != "" and company.application_deadline != None:
					app_deadline = company.application_deadline.strftime('%Y-%m-%d')
				# print "company edit"
			else:
				# print "company name in data"
				c_name = data.get('company_name')
				company = request.user.company_set.get(name=c_name)
				if company.application_deadline != "" and company.application_deadline != None:
					app_deadline = company.application_deadline.strftime('%Y-%m-%d')
				
			contacts = Contact.objects.filter(user=request.user, employer=c_name)
			
			for e in request.user.events.all():
				for c in e.companies.split(','):
					if c.strip() == company.name:
						company.events.add(e)
			
			
			
			events = company.events.all()
			notes = company.notes

			link = company.link
			has_link = False
			if link != '':
				has_link = True

			# print "has link's value is " + str(has_link)
			# print "link = " + link
			context = {'company_edit': company_edit, 'companies': companies, 'company_name': company.name, 
			'application_deadline': app_deadline, 'status': company.application_status, 'show': show_company,
			'contacts': contacts, 'company_notes': company.notes, 'upload_form': upload_form, 'username': request.user.username, 
			'events': events, 'link': link, 'has_link': has_link, "controlled_channels": request.user.controlledChannels}

		else:
			print "got to the else"
			'''
			for company in companies:
				if company.name in data:
					company.delete()
					c_name = company.name
					break

			events = request.user.profile.events.all()
			for event in events:
				
				if c_name == event.title:
					event.delete()
					break
			'''

			# app_deadline = company.application_deadline
			# app_deadline = str(app_deadline)
			# datetime.strptime(app_deadline, "%Y-%m-%d")

			companies = request.user.company_set.all()
			context = {'companies': companies, 'username': request.user.username, 'upload_form': upload_form, "controlled_channels": request.user.controlledChannels}
	else:
		print 'else'
		if company_name != 'all':
			company = request.user.company_set.get(name=company_name)
			contacts = Contact.objects.filter(user=request.user, employer=company_name)
			events = company.events.all()

			app_deadline = company.application_deadline
			app_deadline = str(app_deadline)
			datetime.strptime(app_deadline, "%Y-%m-%d")

			context = {'companies': companies, 'company_name': company.name, 'events': events,			
			'application_deadline': app_deadline, 'show': show_company,
			'contacts': contacts, 'company_notes': company.notes, 'upload_form': upload_form, 'username': request.user.username, "controlled_channels": request.user.controlledChannels}

	return render(request, 'jam/companies/companies.html', context)

def is_valid_date(date):
	now = datetime.now()

	if(date == "" or len(date) == 0):
		return ""

	year = int(date[0:4])
	month = int(date[5:7])
	day = int(date[8:10])


	if(len(date) < 10):
		return "Please enter a date in YYYY-MM-DD format"
	elif ((year < now.year) or (month < now.month) and (year == now.year)) or  ((month == now.month) and (year == now.year) and (day < now.day)):
		return 'You cannot enter a date that is in the past.'
	elif ( month >  12 or day > 31):
		return 'You must enter a valid date. Please try again.'

	return ""

def read_from_file(user, input_file):
	print "in read_from_file"
	for line in input_file:
		if len(line) > 0:
			company_info = line.split(',')
			company_name = company_info[0]
			company_deadline = company_info[1].strip()

			stripped_deadline = company_deadline.replace("-", "")
			stripped_deadline.replace('/', "")
			if len(stripped_deadline) < 8: 
				continue
			elif stripped_deadline.isdigit():
				is_valid_date(company_deadline)
			else:
				continue


			company = Company(name=company_name,
						  application_deadline=company_deadline,
						  user=user)
			company.save()
	return True
