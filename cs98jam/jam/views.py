from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from jam.forms import UploadFileForm
from jam.input import read_from_file
from django.conf import settings
import os

from jam.models import Contact, Company, Profile, Channel, ChannelAdminNote, UserProfile
from django.http import HttpResponseRedirect

from swingtime import utils, forms
from dateutil import parser
from django import http
import calendar
from datetime import datetime, timedelta, time
from swingtime.models import Occurrence, Event
from itertools import chain, groupby
from django.db import models

# Create your views here.
@login_required
def index(request):
	context = {'username': request.user.username}
		
	
	# show only channels in sidebar that user is subscribed to
	channels = request.user.channel_set.order_by("name").all()

	notificationList = []
	for c in channels:
		newNotes = 0
		for note in c.adminNotes.all():
			if note.created_at > request.user.last_login:
				newNotes += 1
		notificationList.append(newNotes)	
	
	show_feed = False    # if true, show newsfeed. else, show regular homepage

	if request.method == "GET":
		form = UploadFileForm()
		site = settings.DOMAIN
		c_name = ""
		context = {'username': request.user.username, 'form': form, 'site': site, 'channels': channels, 
			'show': show_feed ,'events': events, 'notificationList': notificationList}

    #post request can mean 2 things.
    #either a request to see a channel's newsfeed
    #or a request to main homepage view
	elif request.method == "POST":
		show_feed = True
		form_data = request.POST

    	# if user clicked go home, show main homepage
		go_home = form_data.get('back_home')
		if( go_home == ("Go home, Roger!")):
			show_feed = False
			context = {'username': request.user.username, 
			'channels': channels,'show': show_feed, 'events': events, 'notificationList': notificationList}
    	# otherwise, showing clicked channel feed
		else:
			print 'here'
			c_name = form_data.get('channel_name')
			channel = get_object_or_404(Channel, name=c_name)
    	
			is_admin = False
			if request.user.controlledChannels.filter(name=channel.name).exists():
				is_admin = True

			context = {'channel_name': channel.name, 'channel_nickname': channel.moniker,
				'channel_description': channel.description, 'channel_status': channel.is_public, 'notificationList': notificationList, 
				'is_admin': is_admin, 'username': request.user.username, 'channels': channels, 'show': show_feed, 
				"adminNotes": channel.adminNotes.order_by("-created_at")}
            

	return render(request, 'jam/index_landing_home.html', context)


@login_required
def profile(request):
	import pdb;
	form_data = request.POST

	username = request.user.username
	#pdb.set_trace()
	user = User.objects.get(username=username.lower())
	if user:
		try:
			profile = Profile.objects.get(user=username)
		except ObjectDoesNotExist:
			profile = None
	if form_data:
		if user and profile: #already contained in DB, want to edit
			profile.first_name=form_data.get('first_name')
			profile.last_name=form_data.get('last_name')
			profile.email=form_data.get('email')
			profile.phone_number=form_data.get('phone')
			profile.address=form_data.get('address')
			profile.city=form_data.get('city')
			profile.state=form_data.get('state')
			profile.zip_code=form_data.get('zip_code')
			profile.gender=form_data.get('gender')
			profile.school=form_data.get('school_number')
			profile.grad_month=form_data.get('grad_month')
			profile.grad_year=form_data.get('grad_year')


		else:
			profile = Profile(user=request.user.username,
							  first_name=form_data.get('first_name'),
							  last_name=form_data.get('last_name'),
							  email=form_data.get('email'),
							  phone_number=form_data.get('phone'),
							  address=form_data.get('address'),
							  city=form_data.get('city'),
							  state=form_data.get('state'),
							  zip_code=form_data.get('zip_code'),
							  gender=form_data.get('gender'),
							  school=form_data.get('school_number'),
							  grad_month=form_data.get('grad_month'),
							  grad_year=form_data.get('grad_year'))

		profile.save()

		return render(request, 'jam/index.html', {})

	context = {'profile': profile}
	return render(request, 'jam/profile.html', context)

@login_required
def new_channel(request):
	if request.method == 'POST':
		form_data = request.POST
		
		if form_data.get('name') != "" and Channel.objects.filter(name=form_data.get('name')) == None:
			channel = Channel(name=form_data.get('name'), 
				moniker=form_data.get('moniker'), 
				description=form_data.get('description'), 
				is_public=(form_data.get('is_public')), 
				categories="technology")
			channel.save()
			channel.categories
			channel.get_categories_display()
			channel.subscribers.add(request.user)
			channel.admins.add(request.user)
		else:
			errors = ""
			if Channel.objects.filter(name=form_data.get('name')) != None:
				errors = "A channel with that name already exists: please choose another."
			context = {"errors": errors}
			
			return render(request, 'jam/new_channel.html', context)
			
		return HttpResponseRedirect("/jam/")

	else:
		return render(request, 'jam/new_channel.html')

def new_contact(request):
	form_data = request.POST
	contact = Contact(name=form_data.get('name'),
					  phone_number=form_data.get('phone'),
					  email=form_data.get('email'),
					  employer=form_data.get('company'),
					  notes=form_data.get('notes'),
					  user=request.user)
	contact.save()
	return HttpResponse()

@login_required
def activate_subscriber(request, channel_name, user_name):
	channel = get_object_or_404(Channel, name=channel_name)

	# assume invalid until proven otherwise...
	# only add new subscriber if this person is REALLY an admin ;)
	is_admin = False
	if request.user in channel.admins.all():
		is_admin = True
		user = get_object_or_404(User, username=user_name)
		channel.subscribers.add(user)

	# pass the appropriate context to populate generic activation view
	context = {'channel_name': channel.name, 'username': user_name, 'valid': is_admin, 'site': settings.DOMAIN}
	return render(request, 'jam/activate_subscriber.html', context)


# Shows the details of a channel. View differs based on whether the channel is public
# or private and the user's status within the channel.
#
# Inputs: request, channel_name (name of the channel to be viewed)
@login_required
def view_channel(request, channel_name):
	channel = get_object_or_404(Channel, name=channel_name)

	is_subscriber = False
	if request.user.channel_set.filter(name=channel_name).exists():
		is_subscriber = True

	is_admin = False
	if request.user.controlledChannels.filter(name=channel_name).exists():
		is_admin = True

	context = {'channel_name': channel.name, 'channel_nickname': channel.moniker,
		'channel_description': channel.description, 'channel_status': channel.is_public, 'is_subscriber': is_subscriber,
		'is_admin': is_admin}

	if request.method == 'POST':
		if 'Unsubscribe' in request.POST:
			channel.subscribers.remove(request.user)
		elif channel.is_public and 'Subscribe' in request.POST:
			channel.subscribers.add(request.user)
		else:
			site = settings.DOMAIN
			link = site + "/jam/channels/activate/" + channel.name + "/" + request.user.username
			for admin in channel.admins.all():
				subject = channel.name + " Suscriber request!"
				body = request.user.username + " would like to join your channel! Click this link to let them in :)\n" + link
				send_mail(subject,body,'dartmouthjam@gmail.com', [admin.email], fail_silently=False)
		return HttpResponseRedirect("/jam/channels/view/" + channel.name)

	return render(request, 'jam/view_channel.html', context)


# Administrative view for a channel. Allows for removal of subscribers.
#
# Inputs: request, channel_name (name of the channel to be viewed)
@login_required
def view_channel_as_admin(request, channel_name):
	channel = get_object_or_404(Channel, name=channel_name)

	is_admin = False
	if request.user.controlledChannels.filter(name=channel_name).exists():
		is_admin = True

	if is_admin and request.method == 'POST':
		for key in request.POST:
			user = User.objects.filter(username=key).first()
			
			if user is not None and request.POST.get(key) == "Remove" and (not 
					user.controlledChannels.filter(name=channel_name).exists() or user == request.user):
				channel.subscribers.remove(User.objects.filter(username=key).first())
			
			elif user is not None and request.POST.get(key) == "Make Admin" and (not 
					user.controlledChannels.filter(name=channel_name).exists()):
				channel.admins.add(User.objects.filter(username=key).first())

		if 'nickname' in request.POST:
			channel.moniker = request.POST.get('nickname')
		if 'description' in request.POST:
			channel.description = request.POST.get('description')
		if 'newAdminNote' in request.POST:
			channel.adminNotes.add(ChannelAdminNote(home_channel=channel, text = request.POST.get('newAdminNote'), author=request.user))
		channel.save()

		return HttpResponseRedirect("/jam/channels/view_as_admin/" + channel.name)

	context = {'channel_name': channel.name, 'channel_nickname': channel.moniker,
		'channel_description': channel.description, 'channel_status': channel.is_public,
		'is_admin': is_admin, 'subscribers': channel.subscribers, 'adminNotes': channel.adminNotes.order_by("-created_at")}


	return render(request, 'jam/view_channel_as_admin.html', context)

def new_company(request):
	if request.method == "POST" and request.FILES:
		form = UploadFileForm(request.FILES)
		read_from_file(request.user, request.FILES['filep'])
	elif request.method == "POST":
		form_data = request.POST
		company = Company(name=form_data.get('name'),
						  application_deadline=form_data.get('deadline'),
						  notes=form_data.get('company_notes'),
						  user=request.user)
		company.save()
	context = {'username': request.user.username}
	return render(request, 'jam/index_landing_home.html', context)

def new_event(request):
	form_data = request.POST
	event = Event(name=form_data.get('name'),
					  date=form_data.get('date'))
	event.save()
	return HttpResponse()

def companies(request):
	companies = request.user.company_set.all()
	data = request.POST
	show_company = True

	context = {'companies': companies, 'username': request.user.username}

	if(data):
		go_home = data.get('back_home')
		if("export" in data):
			user = request.META['LOGNAME']
			path_name = "/Users/%s/Downloads/" % user
			f = open(os.path.join(path_name, "companies.txt"), "w")
			for company in companies:
				f.write(str(company) + ", " + str(company.application_deadline) + "\n")
			f.close() 

		elif(go_home == ("Back")):
			show_company = False
		elif('company_name' in data):
			c_name = data.get('company_name')
			company = get_object_or_404(Company, name=c_name)

			context = {'companies': companies, 'company_name': company.name, 
			'application_deadline': company.application_deadline, 'show': show_company}
		else:
			#print "delete"
			for company in companies:
				if company.name in data:
					company.delete()
					break
			companies = request.user.company_set.all()
			context = {'companies': companies, 'username': request.user.username}

	return render(request, 'jam/companies.html', context)

def company_page(request, company_name):
	#companies = request.user.com_set.all

	#company = get_object_or_404(Company, name=company_name,user=request.user)
	contacts = Contact.objects.filter(user=request.user, employer=company_name)
	contacts = Contact.objects.filter(user=request.user, employer=company_name)
	events = request.user.profile.events.all()
	context = {'company': 'company', 'contacts': contacts, 'events': events, 'company_name': company_name}
	print "f'in company_page"
	return render(request, 'jam/company_page.html', context)

#@login_required
def edit_company(request, company_name):
	print "got_here"
	form_data = request.POST

	# username = request.user.username

	# user = User.objects.get(username=username.lower())
	# company = get_object_or_404(Company, name=company_name,user=request.user.username)
	# if form_data:
	# 	if user and company: 
	# 		company.name=form_data.get('company_name')
	# 		company.application_deadline=form_data.get('application_deadline')
	# 		company.notes=form_data.get('notes')

	# 	else:
	# 		company = Company(user=request.user.username,
	# 						  company_name=form_data.get('company_name'),
	# 						  application_deadline=form_data.get('application_deadline'),
	# 						  notes=form_data.get('notes'))

	# 	company.save()

	# 	return render(request, 'jam/index.html', {})

	#context = {'company': 'company'}
	return render(request, 'jam/company_page_edit.html')

def contacts(request):
	contacts = request.user.contact_set.all()
	data = request.POST

	if (data):
		if("export" in data): #if we want to output this as text file:
			#import pdb; pdb.set_trace()
			user = request.META['LOGNAME']
			path_name = "/Users/%s/Downloads/" % user
			f = open(os.path.join(path_name, "contacts.txt"), "w")
			for contact in contacts:
				f.write(str(contact) + ", " + str(contact.employer) + "\n")
			f.close()
		else: 
			for c in contacts:
				if c.name in data:
					c.delete()
					break
			contacts = request.user.contact_set.all()

	context = {'contacts': contacts, 'username': request.user.username}
	return render(request, 'jam/contacts.html', context)

def cal(request):
	context = {}
	return render(request, 'jam/calendar.html', context)

def channel_list(request):
	CHANNEL_CATEGORIES = ('Technology', 
		'Business', 
		'Law', 
		'Medicine', 
		'Women'
	)
	channels = Channel.objects.all()
	context={'channels': channels, 'categories': CHANNEL_CATEGORIES, 'username': request.user.username}
	return render(request,'jam/channel_list.html',context)

def test(request):
	context = {}
	return render(request, 'jam/base_companies.html', context)

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
			elif (request.user.controlledChannels.filter(name=channel_name).exists()):
				channel = get_object_or_404(Channel, name=channel_name)
				channel.events.add(event)
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

	return render(
		request,
		template,
		{'dtstart': dtstart, 'event_form': event_form, 'recurrence_form': recurrence_form, 'username': request.user.username}
	)

   ####FROM SWINGWIMG ADD COMENTS

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
	extra_context={'username': request.user.username}
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
   # dtend       = datetime(year, month, last_day)

	#### JAM CODE ####
	my_events = request.user.profile.events.all() #access all of the uers events
	
	
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
		'this_month': dtstart,
		'next_month': dtstart + timedelta(days=+last_day),
		'last_month': dtstart + timedelta(days=-1),
        'username': request.user.username
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
        'username': request.user.username
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
                return http.HttpResponseBadRequest('Bad Request')

        data = {
            'event': event,
            'event_form': event_form or event_form_class(instance=event),
            'recurrence_form': recurrence_form or recurrence_form_class(initial={'dtstart': datetime.now()})
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
    print "TEST"
    if request.user.profile.events.filter(pk=event_pk).exists():
        print "TEST2"
        if request.method == 'POST':
            form = form_class(request.POST, instance=occurrence)
            if form.is_valid():
                form.save()
                return http.HttpResponseRedirect(request.path)
        else:
            form = form_class(instance=occurrence)
        
        return render(request, template, {'occurrence': occurrence, 'form': form})
        
    else:
        return HttpResponseRedirect('/jam/events/')
#-------------------------------------------------------------------------------
	
	
	
#########################################################################################################
# End to swingtime edits!
#########################################################################################################

'''account management page
link to reset password, update email,
and change notification frequency'''
def manage_account(request):
	form_data = request.POST

	site = settings.DOMAIN
	user_profile = UserProfile.objects.filter(user=request.user)

	user = request.user
	context ={'site': site, 'profile': user_profile, 'email': user.email}

	if form_data:
		user.email = form_data.get('new_email')
		user.save()
		freq = form_data.get('notif_freq')
		# figure out notification val
		notifs = 0
		if(freq == "notif_four"):
			notifs = 42
		elif(freq == "notif_daily"):
			notifs = 7
		elif(freq == "notif_weekly"):
			notifs = 1
		user_profile.notification_frequency = notifs
	return render(request, 'jam/manage_account.html', context)
