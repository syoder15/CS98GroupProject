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

from jam.models import Contact, Company, Profile, Channel, ChannelAdminNote, UserProfile, ChannelCategory, EventOccurrence, Event as jam_event
from django.http import HttpResponseRedirect

from swingtime import utils, forms
from swingtime import models as swingmodel
from dateutil import parser
from django import http
import calendar
from datetime import datetime, timedelta, time
from itertools import chain, groupby
from django.db import models
from django.utils import timezone
from dateutil import rrule
from dateutil.relativedelta import relativedelta

upload_form = UploadFileForm

def startEndTimeValidation(start_time, end_time):
	startTime = start_time.split(':')
	endTime = end_time.split(':')
	startMin = startTime[1].split(" ")
	endMin = endTime[1].split(" ")
	error = ''
	print 'python'
	print startTime[0]

	if len(startMin) > 1: 
		if (startMin[1].lower() == 'p.m.'):
			startMin[1] = 'pm'
		if (startMin[1].lower() == 'pm' and int(startTime[0]) is not 12):
			print 'start is not 12 python'
			startTime[0] = int(startTime[0]) + 12
	if len(endMin) > 1:
		if (endMin[1].lower() == 'p.m.'):
			endMin[1] = 'pm'
		if (endMin[1].lower() == 'pm' and int(endTime[0]) is not 12):
			endTime[0] = int(endTime[0]) + 12

	'''if ( endTime[0] < startTime[0] or (endTime[0] == startTime[0] and int(endMin[0]) < int(startMin[0]))):
		error = "Your start time must be before your end time. Please try again."
		print "hit a wall"
	
	'''
	start = str(startTime[0]) + ":" + str(startMin[0])
	end = str(endTime[0]) + ":" + str(endMin[0])

	return (start,end)

def add_recurring_events(request, event, occurrence):
	start_date = datetime.strptime(event.event_date, "%Y-%m-%d")
	end_date = datetime.strptime(occurrence.end_date, "%Y-%m-%d")
	year = int(occurrence.start_year) + 1

	#if occurrence.start_year <= start_date.year && occurrence.start_month <= start_date.month && occurrence.start_day <= start_date.day:
	if occurrence.frequency == "Annually":
		while year <= int(end_date.year):
			date = str(year) + "-" + start_date.strftime("%m") + "-" + start_date.strftime("%d")
			date_datetime = datetime.strptime(date, "%Y-%m-%d")

			if date_datetime < end_date:
				newer_event = jam_event(
					name=event.name,
					event_type=event.event_type,
					description=event.description,
					companies=event.companies,
					event_date=date,
					start_time=event.start_time,
					end_time=event.end_time,
					occurrence_id = occurrence.id,
					creator=event.creator)

				newer_event.save()
				request.user.events.add(newer_event)
				request.user.owned_events.add(newer_event)
			year += 1
		return

	if occurrence.frequency == "Monthly":
		increment = 1

		date_datetime = start_date + relativedelta(months=increment)
		while date_datetime <= end_date:
			newer_event = jam_event(
					name=event.name,
					event_type=event.event_type,
					description=event.description,
					companies=event.companies,
					event_date=date_datetime,
					start_time=event.start_time,
					end_time=event.end_time,
					occurrence_id = occurrence.id,
					creator=event.creator)

			newer_event.save()
			request.user.events.add(newer_event)
			request.user.owned_events.add(newer_event)

			increment += 1
			date_datetime = start_date + relativedelta(months=increment)
		return

	if occurrence.frequency == "Weekly":
		incr = 7
	if occurrence.frequency == "Daily":
		incr = 1

	increment = incr
	date_datetime = start_date + relativedelta(days=increment)
	while date_datetime <= end_date:
		newer_event = jam_event(
					name=event.name,
					event_type=event.event_type,
					description=event.description,
					companies=event.companies,
					event_date=date_datetime,
					start_time=event.start_time,
					end_time=event.end_time,
					occurrence_id = occurrence.id,
					creator=event.creator)

		newer_event.save()
		request.user.events.add(newer_event)
		request.user.owned_events.add(newer_event)

		increment += incr
		date_datetime = start_date + relativedelta(days=increment)

@login_required
def new_event(request):
	if request.method == "POST":
		form_data = request.POST

		event_date = form_data.get('event_date')
		validity = is_valid_date(event_date)

		end_date = form_data.get('end_date')
		end_validity = ''
		if (end_date):
			end_validity = is_valid_date(end_date)

		if(validity!='' and end_validity !=''):
	
			# return bad request if the date is still invalid somehow (but very unlikely!)
			response={}
			response["error"] = validity
			return HttpResponseBadRequest(json.dumps(response),content_type="application/json")
		
		event_name = form_data.get('name')

		startTime, endTime = startEndTimeValidation(form_data.get('start_time'),form_data.get('end_time'))
		#print "start time" + startTime + "end time" + endTime
		if (form_data.get('recurrence') != 'None'):
			date_obj = datetime.strptime(str(form_data.get('event_date')), "%Y-%m-%d")

			occurrence = EventOccurrence(
				name=event_name,
				frequency=form_data.get('recurrence'),
				start_month=form_data.get('event_date')[5:7],
				start_year=form_data.get('event_date')[0:4],
				start_day=form_data.get('event_date')[8:10],
				day_of_the_week=date_obj.strftime('%A'),
				end_date=form_data.get('end_date'))

			print occurrence

			occurrence.save()

			occurrence_id = occurrence.id
			event = jam_event(name=event_name,
						  event_type=form_data.get('event_type'),
						  description=form_data.get('description'),
						  companies=form_data.get('companies'),
						  event_date=form_data.get('event_date'),
						  start_time=startTime,
						  end_time=endTime,
						  occurrence_id = occurrence_id,
						  creator=request.user)

			add_recurring_events(request, event, occurrence)
		else:
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
		request.user.owned_events.add(event)

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
		
		context = {'username': request.user.username}

		return render(request, 'jam/index/index_landing_home.html', context)


def delete_event(request, event_id):
	event = request.user.events.get(id=event_id)
	if event in request.user.owned_events.all():
		owned_event = request.user.owned_events.get(id=event_id)
		owned_event.delete()

		event.delete()
	else:
		request.user.events.remove(event)

def delete_recurring_events(request, occurrence_id, edit_date):
	events = request.user.events.filter(occurrence_id=occurrence_id)

	for e in events:
		if e in request.user.owned_events.all():
			if edit_date and edit_date <= e.event_date:
				delete_event(request, e.id)
			elif edit_date == None:
				delete_event(request, e.id)
			else:
					e.occurrence_id = None
					e.save()
		else:
			request.user.events.remove(e)

	if events[0] in request.user.owned_events.all():
		occurrence = EventOccurrence.objects.filter(id=occurrence_id).first()
		occurrence.delete()

@login_required
def events_page(request, event_id, event_name):
	data = request.POST
	events = request.user.events.all()
	#event = request.user.events.filter(id=event_id)
	event = request.user.events.get(id=event_id)
	if event in request.user.owned_events.all():
		owned = True
	else:
		owned = False

	event_type = event.event_type
	event_description = event.description
	event_date = event.event_date
	start_time = event.start_time
	end_time = event.end_time

	recurrence_object = EventOccurrence.objects.filter(id=event.occurrence_id).first() #first?
	if recurrence_object:
		recurrence = recurrence_object.frequency
		show_delete_all = True
		occurrence_id = event.occurrence_id
		
		end_date = recurrence_object.end_date
		end_date = str(end_date)
		datetime.strptime(end_date, "%Y-%m-%d")
	else:
		recurrence = 'None'
		show_delete_all = False
		occurrence_id = None
		end_date = None

	if (event_type == 'app'): 
		event_type = 'Application Deadline'

	event_title = urlify(event_name)
	event_desc = urlify(event_description)
	google_link = "http://www.google.com/calendar/event?action=TEMPLATE&text=" + event_title + "&dates=" + str(event_date.year) + str(event_date.month).zfill(2) + str(event_date.day).zfill(2) + "T" + str(start_time.hour +5).zfill(2) + str(start_time.minute).zfill(2) + "00Z/" + str(event_date.year) +  str(event_date.month).zfill(2) + str(event_date.day).zfill(2) + "T" + str(end_time.hour + 5).zfill(2) + "" +  str(end_time.minute).zfill(2) + "00Z&details=" + event_desc

	company_text = event.companies
	if company_text:
		comps = company_text.split(",")
	else:
		comps = ''

	companies = []
	non_companies = []
	for c in comps:
		if request.user.company_set.filter(name=c).exists():
 			companies.append(c)
 		else:
 			non_companies.append(c)

 	
 	
 	if('delete' in data):
 		delete_event(request, event_id)
 		
 		month = str(event_date)[5:7]
 		year = str(event_date)[0:4]
 		link = "/jam/calendar/" + str(year) + '/' + str(month)
 		
 		return HttpResponseRedirect(link)

 	if('delete_all' in data):
 		delete_recurring_events(request, event.occurrence_id, None)
 		month = str(event_date)[5:7]
 		year = str(event_date)[0:4]
 		link = "/jam/calendar/" + str(year) + '/' + str(month)
 		
 		return HttpResponseRedirect(link)

	context = {'events': events, 'event': event, 'event_name': event_name, 'event_description': event_description, 'event_date': event_date,
	'start_time': start_time.strftime("%I:%M %p"), 'end_time': end_time.strftime("%I:%M %p"), 'event_type': event_type, 
	'google_link': google_link, "controlled_channels": request.user.controlledChannels, 
	'companies': companies, 'other_comp': non_companies, 'recurrence': recurrence, 'delete_button': show_delete_all, 'occurrence_id': occurrence_id, 
	'event_id': event.id, 'end_date': end_date, 'owned_event': owned}

	return render(request, 'events/event_detail_page.html', context)

@login_required
def edit_event(request, event_id):
	form_data = request.POST

	user = User.objects.get(username=request.user.username)
	event = request.user.events.get(id=event_id)

	if form_data:
		startTime, endTime = startEndTimeValidation(form_data.get('start_time'),form_data.get('end_time'))

		if "Save_All" in form_data:
			if request.POST.get("occurrence_id"):
				occurrence_id = int(request.POST.get("occurrence_id"))

				delete_recurring_events(request, occurrence_id, event.event_date)
				new_event(request)

				datetime_obj = event.event_date
				redirect_link = '../../../calendar/' +  datetime_obj.strftime('%Y') + '/' + datetime_obj.strftime('%m')
				return HttpResponseRedirect(redirect_link)

		if user and event:
			event.name=form_data.get('name')
			event.event_type=form_data.get('event_type')
			event.description=form_data.get('description')
			event.companies=form_data.get('companies')
			event.event_date=form_data.get('event_date')
			event.start_time=startTime
			event.end_time=endTime
			event.save()

			datetime_obj = datetime.strptime(event.event_date, "%Y-%m-%d")
			redirect_link = '../../../calendar/' +  datetime_obj.strftime('%Y') + '/' + datetime_obj.strftime('%m')
			return HttpResponseRedirect(redirect_link)

		else:
			event = jam_event(name=form_data.get('name'),
						  event_type=form_data.get('event_type'),
						  description=form_data.get('description'),
						  companies=form_data.get('companies'),
						  event_date=form_data.get('event_date'),
						  start_time=startTime,
						  end_time=endTime,
						  creator=request.user)
			event.save()
			request.user.events.add(event)
			request.user.owned_events.add(event)

			datetime_obj = datetime.strptime(event.event_date, "%Y-%m-%d")
			redirect_link = '../../../calendar/' +  datetime_obj.strftime('%Y') + '/' + datetime_obj.strftime('%m')
			return HttpResponseRedirect(redirect_link)

	event_date = event.event_date
	event_date = str(event_date)
	datetime.strptime(event_date, "%Y-%m-%d")

	if event.occurrence_id:
		delete_button = True
		recurrence_object = EventOccurrence.objects.filter(id=event.occurrence_id).first()
		recurrence = recurrence_object.frequency
		
		end_date = recurrence_object.end_date
		end_date = str(end_date)
		datetime.strptime(end_date, "%Y-%m-%d")
	else:
		delete_button = False
		recurrence = None
		end_date = None

	context = {'event': event, 'event_name': event.name, 'description': event.description, 'event_date': event_date,
	'start_time': event.start_time.strftime("%I:%M %p"), 'end_time': event.end_time.strftime("%I:%M %p"), 'creator': event.creator, 'event_type': event.event_type, 
	'companies': event.companies, "delete_button": delete_button, 'recurrence': recurrence, 'end_date': end_date,
	'occurrence_id': event.occurrence_id}

	return render(request, 'events/event_edit.html', context)



@login_required
def month_view(
	request,
	year,
	month,
	template='events/monthly_view.html',
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

	if len(str(month)) < 2:
		month = '-0' + str(month) + '-'
	else:
		month = "-" + str(month) + "-"
	#### JAM CODE ####
	
	my_events = request.user.events.filter(event_date__contains=month) #access all of the users events

	my_new_events = request.user.profile.events.none()
	if request.method == "POST":
		if request.POST.get('Interviews'):
			my_new_events = my_events.filter(event_type = 'Interview') | my_new_events
		else:
			interview = False

		if request.POST.get('Career Fairs'):
			my_new_events = my_events.filter(event_type = 'Career Fair') | my_new_events
		else:
			careerFair = False

		if request.POST.get('Application Deadline'):
			my_new_events = my_events.filter(event_type = 'Application Deadline') | my_new_events
		else:
			app_deadline = False

		if request.POST.get('Info Sessions'):
			my_new_events = my_events.filter(event_type = 'Info Session') | my_new_events
		else:
			infoSession = False

		if request.POST.get('Other'):
			my_new_events = my_events.filter(event_type = 'Other') | my_new_events
		else:
			other = False
		my_events = my_new_events

	def start_date(o):
		return o.event_date.day

	def start_month(o):
		return o.event_date.month

	by_day = dict([(dt, list(o)) for dt,o in groupby(my_events, start_date)])
	
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
		'upload_form' : upload_form,
		"controlled_channels": request.user.controlledChannels
	}

	return render(request, template, data)

@login_required
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
@login_required
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
@login_required
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
@login_required
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
