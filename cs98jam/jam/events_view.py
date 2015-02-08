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

upload_form = UploadFileForm

######################################################################################
# The following views were taken from django swingtime: https://github.com/dakrauth/django-swingtime
# We made slight edits which include comments below. These edits were made in order to allow user-specific
# calendars for our Events page
######################################################################################
def add_event(
	request,
	template='swingtime/add_event.html',
	event_form_class=forms.EventForm,
	recurrence_form_class=forms.MultipleOccurrenceForm,
	channel_name = None
):
	'''
	Add a new ``Event`` instance and 1 or more associated ``Occurrence``s.

	Context parameters:

	dtstart
		a datetime.datetime object representing the GET request value if present,
		otherwise None

	event_form
		a form object for updating the event

	recurrence_form
		a form object for adding occurrences

	'''
	dtstart = None
	if request.method == 'POST':
		event_form = event_form_class(request.POST)
		recurrence_form = recurrence_form_class(request.POST)
		if event_form.is_valid() and recurrence_form.is_valid():
			event = event_form.save()
			
			#### JAM CODE ####
			if (not channel_name):
				user_profile = get_object_or_404(UserProfile, user=request.user) ##grab the user profile which we will add events to
				user_profile.events.add(event) #associate the current event with a user's profile
				user_profile.owned_events.add(event)

				company_field = request.POST.get('description')
				company_field = company_field.replace(" ", "")
				companies = company_field.split(',')
				for c in companies:
					if len(request.user.company_set.filter(name=c)) > 0:
						company = request.user.company_set.filter(name=c)
						company = company[0]
						company.events.add(event)

			elif (request.user.controlledChannels.filter(name=channel_name).exists()):
				channel = get_object_or_404(Channel, name=channel_name)
				channel.events.add(event)
				for user in channel.admins.all():
					user.profile.owned_events.add(event)
					user.profile.events.add(event)
				
			#### JAM CODE ####	
			recurrence_form.save(event)
			return http.HttpResponseRedirect(event.occurrence_set.first().get_absolute_url())
	else:
		if 'dtstart' in request.GET:
			try:
				dtstart = parser.parse(request.GET['dtstart'])
			except:
				# TODO A badly formatted date is passed to add_event
				pass

		dtstart = dtstart or datetime.now()
		event_form = event_form_class()
		recurrence_form = recurrence_form_class(initial={'dtstart': dtstart})

		#print recurrence_form


	return render(
		request,
		template,
		{'dtstart': dtstart, 'event_form': event_form, 'recurrence_form': recurrence_form, 'username': request.user.username}
	)

def startEndTimeValidation(start_time, end_time):
	startTime = start_time.split(':')
	endTime = end_time.split(':')
	startMin = startTime[1].split(" ")
	endMin = endTime[1].split(" ")

	error = ''
	print "about to convert"
	if (startMin[1].lower() == 'pm'):
		startTime[0] = int(startTime[0]) + 12
		print "first block"
	if (endMin[1].lower() == 'pm'):
		endTime[0] = int(endTime[0]) + 12
		print "second block"

	'''if ( endTime[0] < startTime[0] or (endTime[0] == startTime[0] and int(endMin[0]) < int(startMin[0]))):
		error = "Your start time must be before your end time. Please try again."
		print "hit a wall"
	
	'''
	print "ugh"
	start = str(startTime[0]) + ":" + str(startMin[0])
	end = str(endTime[0]) + ":" + str(endMin[0])

	print "ish"
	print "inside startEnd validation"
	return (start,end)

def new_event(request):
	if request.method == "POST":
		form_data = request.POST

		event_date = form_data.get('event_date')
		validity = is_valid_date(event_date)
		print "validity is " + validity
		if(validity!=''):
	
			# return bad request if the date is still invalid somehow (but very unlikely!)
			response={}
			response["error"] = validity
			print "got here"
			return HttpResponseBadRequest(json.dumps(response),content_type="application/json")
		
		event_name = form_data.get('name')

		startTime, endTime = startEndTimeValidation(form_data.get('start_time'),form_data.get('end_time'))
		#print "start time" + startTime + "end time" + endTime

		event = jam_event(name=event_name,
						  event_type=form_data.get('event_type'),
						  description=form_data.get('description'),
						  companies=form_data.get('companies'),
						  event_date=form_data.get('event_date'),
						  start_time=startTime,
						  end_time=endTime,
						  creator=request.user)
		event.save()
		request.user.events.add(event)

		if request.user.controlledChannels.filter(name=form_data.get("channel")).exists():
			channel = request.user.controlledChannels.filter(name=form_data.get("channel")).first()
			if form_data.get("channel") != "None":
				event.channel_set.add(channel)
		
		company_field = form_data.get('companies')
		if company_field != '':
			company_field = company_field.replace(" ", "")
			companies = company_field.split(',')
			for c in companies:
				if len(request.user.company_set.filter(name=c)) > 0:
					company = request.user.company_set.filter(name=c)
					company = company[0]
					company.events.add(event)
		#user_profile = get_object_or_404(UserProfile, user=request.user) ##grab the user profile which we will add events to
		#user_profile.events.add(event) #associate the current event with a user's profile
		#user_profile.owned_events.add(event)
		
		context = {'username': request.user.username}

		return render(request, 'jam/index/index_landing_home.html', context)

def events_page(request, event_id, event_name):
	events = request.user.events.all()
	#event = request.user.events.filter(id=event_id)
	event = request.user.events.get(id=event_id)
	
	event_type = event.event_type
	event_description = event.description
	event_date = event.event_date
	start_time = event.start_time
	end_time = event.end_time

	if event_type == 'fair': 
		event_type = 'Career Fair'
	if (event_type == 'int'):
		event_type = 'Interview'
	if (event_type == 'app'): 
		event_type = 'Application Deadline'
	if (event_type == 'other'): 
		event_type = 'Other'
	if (event_type == 'info'): 
		event_type = 'Info Session'

	context = {'events': events, 'event_name': event_name, 'event_description': event_description, 'event_date': event_date,
	'start_time': start_time, 'end_time': end_time, 'event_type': event_type}

	return render(request, 'swingtime/event_detail_page.html', context)


####FROM SWINGTIME ADD COMMENTS

def event_listing(
	request,
	template='swingtime/event_list.html',
	events=None,
	**extra_context
):
	'''
	View all ``events``.

	If ``events`` is a queryset, clone it. If ``None`` default to all ``Event``s.

	Context parameters:

	events
		an iterable of ``Event`` objects

	???
		all values passed in via **extra_context
	'''
	extra_context={'username': request.user.username, 'upload_form': upload_form}
	return render(
		request,
		template,
		dict(extra_context, events=events or request.user.profile.events.all()),
		
		#changed request.user.profile.events.all() to Event.objects.all() in order to only grab the current user's events
	)



def month_view(
	request,
	year,
	month,
	template='swingtime/monthly_view.html',
	queryset=None
):
	'''
	Render a tradional calendar grid view with temporal navigation variables.

	Context parameters:

	today
		the current datetime.datetime value

	calendar
		a list of rows containing (day, items) cells, where day is the day of
		the month integer and items is a (potentially empty) list of occurrence
		for the day


	this_month
		a datetime.datetime representing the first day of the month

	next_month
		this_month + 1 month

	last_month
		this_month - 1 month

	'''
	year, month = int(year), int(month)
	cal         = calendar.monthcalendar(year, month)
	dtstart     = datetime(year, month, 1)
	last_day    = max(cal[-1])
	interview   = True
	careerFair  = True
	infoSession = True
	app_deadline= True
	other       = True
    # dtend       = datetime(year, month, last_day)

	#### JAM CODE ####
	my_events = request.user.profile.events.all() #access all of the users events
	my_events = []

	for e in request.user.events.all():
		e_month = e.event_date.month
		if month is e_month:
			my_events.append(e)

	#my_events = request.user.events.all()
	print my_events
	my_new_events = request.user.profile.events.none()
	if request.method == "POST":
		if request.POST.get('Interviews'):
			my_new_events = my_events.filter(event_type = 'int') | my_new_events
		else:
			interview = False

		if request.POST.get('Career Fairs'):
			my_new_events = my_events.filter(event_type = 'fair') | my_new_events
		else:
			careerFair = False

		if request.POST.get('Application Deadline'):
			my_new_events = my_events.filter(event_type = 'app') | my_new_events
		else:
			app_deadline = False

		if request.POST.get('Info Sessions'):
			my_new_events = my_events.filter(event_type = 'info') | my_new_events
		else:
			infoSession = False

		if request.POST.get('Other'):
			my_new_events = my_events.filter(event_type = 'other') | my_new_events
		else:
			other = False

		my_events = my_new_events

	def start_date(o):
		return o.event_date.day

	def start_month(o):
		return o.event_date.month

	by_day = dict([(dt, list(o)) for dt,o in groupby(my_events, start_date)])
	#by_day = dict([(m, dt) for m,dt in groupby(start_month, start_date)])
	
	data = {
		'today'		  : datetime.now(),
		'calendar'	  : [[(d, by_day.get(d, [])) for d in row] for row in cal],
		'username'	  : request.user.username,
		'this_month'  : dtstart,
		'next_month'  : dtstart + timedelta(days=+last_day),
		'last_month'  : dtstart + timedelta(days=-1),
		'interview'   : interview,
		'careerFair'  : careerFair,
		'infoSession' : infoSession,
		'app_deadline': app_deadline,
		'other'		  : other,
		'upload_form' : upload_form
	}

	return render(request, template, data)

def year_view(request, year, template='swingtime/yearly_view.html', queryset=None):
	'''


	Context parameters:

	year
		an integer value for the year in question

	next_year
		year + 1

	last_year
		year - 1


	by_month
		a sorted list of (month, occurrences) tuples where month is a
		datetime.datetime object for the first day of a month and occurrences
		is a (potentially empty) list of values for that month. Only months
		which have at least 1 occurrence is represented in the list

	'''

	year = int(year)
	my_events = request.user.profile.events.all()
	for event in my_events:  #access all of the uers events
		if queryset == None:
			queryset = event.occurrence_set.all()
		else:
			queryset = queryset | event.occurrence_set.all()

	if queryset == None:
		queryset = Occurrence.objects.filter(start_time = "1970-01-01 00:00")        
			  
	occurrences = queryset.filter(
		models.Q(start_time__year=year) |
		models.Q(end_time__year=year)
	)
	
	def group_key(o):
		return datetime(
			year,
			o.start_time.month if o.start_time.year == year else o.end_time.month,
			1
		)

	return render(request, template, {
		'year': year,
		'by_month': [(dt, list(o)) for dt,o in groupby(occurrences, group_key)],
		'next_year': year + 1,
		'last_year': year - 1,
		'username': request.user.username,
		'upload_form': upload_form
	})

#-------------------------------------------------------------------------------

def event_view(
	request, 
	pk, 
	template='swingtime/event_detail.html', 
	event_form_class=forms.EventForm,
	recurrence_form_class=forms.MultipleOccurrenceForm
):
	'''
	View an ``Event`` instance and optionally update either the event or its
	occurrences.

	Context parameters:

	event
		the event keyed by ``pk``
		
	event_form
		a form object for updating the event
		
	recurrence_form
		a form object for adding occurrences
	'''
	event = get_object_or_404(Event, pk=pk)
	event_form = recurrence_form = None
	if request.user.profile.events.filter(pk=pk).exists():
		event_owned = False;
		if request.user.profile.owned_events.filter(pk=pk).exists():
			event_owned = True;
	
		if request.method == 'POST':
			if '_update' in request.POST:
				event_form = event_form_class(request.POST, instance=event)
				if event_form.is_valid():
					event_form.save(event)
					return http.HttpResponseRedirect(request.path)
			elif '_add' in request.POST:
				recurrence_form = recurrence_form_class(request.POST)
				if recurrence_form.is_valid():
					recurrence_form.save(event)
					return http.HttpResponseRedirect(request.path)
			else:
				events = request.user.profile.events.all()
				for event in events:
					if request.POST.get('title') == event.name:
						event.delete()
						break
				return month_view(request, datetime.today().year, datetime.today().month)

		data = {
			'event': event,
			'event_form': event_form or event_form_class(instance=event),
			'recurrence_form': recurrence_form or recurrence_form_class(initial={'dtstart': datetime.now()}),
			'owned': event_owned,

			'upload_form': upload_form

		}
		return render(request, template, data)
	else:
		return HttpResponseRedirect("/jam/events")

#-------------------------------------------------------------------------------
def occurrence_view(
	request, 
	event_pk, 
	pk, 
	template='swingtime/occurrence_detail.html',
	form_class=forms.SingleOccurrenceForm
):
	'''
	View a specific occurrence and optionally handle any updates.
	
	Context parameters:
	
	occurrence
		the occurrence object keyed by ``pk``

	form
		a form object for updating the occurrence
	'''
	occurrence = get_object_or_404(Occurrence, pk=pk, event__pk=event_pk)

	if request.user.profile.events.filter(pk=event_pk).exists():
		event_owned = False;
		if request.user.profile.owned_events.filter(pk=pk).exists():
			event_owned = True;
		

		if request.method == 'POST':
			form = form_class(request.POST, instance=occurrence)
			if form.is_valid():
				form.save()
				return http.HttpResponseRedirect(request.path)
		else:
			form = form_class(instance=occurrence)

		#google calendar link shenanigans		
		st = occurrence.start_time
		et = occurrence.end_time

		'''title_list = occurrence.title.split(' ')
		event_title = ""
		i = 0
		for word in title_list:
			i+=1
			if i != (len(title_list)):
				event_title = event_title + word + "+"
			else:
				event_title += word
		'''
		event_title = urlify(occurrence.title)
		event_desc = urlify(occurrence.event.description)
		google_link = "http://www.google.com/calendar/event?action=TEMPLATE&text=" + event_title + "&dates=" + str(st.year) + str(st.month).zfill(2) + str(st.day).zfill(2) + "T" + str(st.hour +5).zfill(2) + str(st.minute).zfill(2) + "00Z/" + str(et.year) +  str(et.month).zfill(2) + str(et.day).zfill(2) + "T" + str(et.hour + 5).zfill(2) + "" +  str(et.minute).zfill(2) + "00Z&details=" + event_desc

		return render(request, template, {'occurrence': occurrence, 'form': form, 'upload_form': upload_form, 'google': google_link, 'owned': event_owned})

		
	else:
		return HttpResponseRedirect('/jam/events/')
#-------------------------------------------------------------------------------
	
def urlify(desc):
	word_list = desc.split(' ')
	url = ''

	i = 0
	for word in word_list:
		i+=1
		if i != len(word_list):
			url = url + word + '+'
		else:
			url += word
	return url

def is_valid_date(date):
	now = datetime.now()

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

	
#########################################################################################################
# End to swingtime edits!
#########################################################################################################
