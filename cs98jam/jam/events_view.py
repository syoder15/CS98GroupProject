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
			return http.HttpResponseRedirect(event.get_absolute_url())
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

   ####FROM SWINGWIME ADD COMENTS

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
	queryset=None,
	filters='false'
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
	other       = True
   # dtend       = datetime(year, month, last_day)

	#### JAM CODE ####
	my_events = request.user.profile.events.all() #access all of the uers events
	my_new_events = request.user.profile.events.none()
	if request.method == "POST":
		if request.POST.get('Interviews') or filters is 'true' :
			my_new_events = my_events.filter(event_type_id = 1) | my_new_events
		else:
			interview = False

		if request.POST.get('Career Fairs') or filters is 'true' :
			my_new_events = my_events.filter(event_type_id = 2) | my_new_events
		else:
			careerFair = False

		if request.POST.get('Info Sessions') or filters is 'true' :
			my_new_events = my_events.filter(event_type_id = 3) | my_new_events
		else:
			infoSession = False

		if request.POST.get('Other') or filters is 'true' :
			my_new_events = my_events.filter(event_type_id = 4) | my_new_events
		else:
			other = False

		my_events = my_new_events


	
	for event in my_events: #loop through the users events and create a queryset of all of the occurances
		if queryset == None:
			queryset = event.occurrence_set.all()
		else:
			queryset = queryset | event.occurrence_set.all()
	
	if queryset == None:
		queryset = queryset._clone() if queryset else Occurrence.objects.filter(start_time = "1970-01-01 00:00")
	
	#### JAM CODE ####

	occurrences = queryset.filter(start_time__year=year, start_time__month=month)

	def start_day(o):
		return o.start_time.day

	by_day = dict([(dt, list(o)) for dt,o in groupby(occurrences, start_day)])
	data = {
		'today':      datetime.now(),
		'calendar':   [[(d, by_day.get(d, [])) for d in row] for row in cal],
		'username': request.user.username,
		'this_month' : dtstart,
		'next_month' : dtstart + timedelta(days=+last_day),
		'last_month' : dtstart + timedelta(days=-1),
		'interview'  : interview,
		'careerFair' : careerFair,
		'infoSession': infoSession,
		'other'		 : other,
		'upload_form'		 : upload_form
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
					if request.POST.get('title') == event.title:
						event.delete()
						break
				return month_view(request, datetime.today().year, datetime.today().month, 'swingtime/monthly_view.html', None, 'true')

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

	
#########################################################################################################
# End to swingtime edits!
#########################################################################################################
