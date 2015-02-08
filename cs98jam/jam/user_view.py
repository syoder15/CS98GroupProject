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
#import pytz
#import newspaper

upload_form = UploadFileForm

# Create your views here.
@login_required
def index(request):
	#context = {'username': request.user.username}

	#money_articles = newspaper.build('http://money.cnn.com/')
	#import pdb; pdb.set_trace()
	article_images = []
	article_urls = {}
	
	'''i = 0
	for article in money_articles.articles:
		if i == 10:
			break
		article.download()
		article.parse()
		if article.title != "404 Page Not Found" and article.title != "Error":
			article_urls[article.url] = article.title
		i += 1
	'''
	events = request.user.events.all()
	future_events = []
	for e in events:
		if (e.event_date >= datetime.now().date()):
			if (e.event_date == datetime.now().date()) and (e.start_time <= datetime.now().time()):
				continue #if the event already happened today, don't add it
			future_events.append(e)
	# show only channels in sidebar that user is subscribed to
	channels = request.user.channel_set.order_by("name").all()

	companies = request.user.company_set.order_by("application_deadline").all()

	notificationList = []
	for c in channels:
		newNotes = 0
		for note in c.adminNotes.all():
			if note.created_at > request.user.last_login:
				newNotes += 1
		notificationList.append(newNotes)	

	# application status notifications
	app_notifications = []
	for c in companies:
		if c.application_deadline <= datetime.today().date() + timedelta(days=2) and not c.application_status:
			if c.application_deadline == datetime.today().date():
				app_notifications.append("Your " + c.name + " application is due today. Get on that ASAP!")
			elif c.application_deadline == datetime.today().date() + timedelta(days=1):
				app_notifications.append("Your " + c.name + " application is due tomorrow. Get on that ASAP!")
			else: 
				app_notifications.append("Your " + c.name + " application is due in two days. Get on that ASAP!")

	show_feed = False    # if true, show newsfeed. else, show regular homepage

	if request.method == "GET":
	
		site = settings.DOMAIN
		c_name = ""

		context = {'username': request.user.username, 'upload_form': upload_form, 'site': site, 
			'channels': channels, 'show': show_feed ,'events': future_events, 'notificationList': notificationList, 'app_list': app_notifications,
			'article_urls': article_urls, 'article_images': article_images, "controlled_channels": request.user.controlledChannels}

	#post request can mean 2 things.
	#either a request to see a channel's newsfeed
	#or a request to main homepage view
	elif request.method == "POST":
		show_feed = True
		form_data = request.POST
		
		# if user clicked go home, show main homepage
		go_home = form_data.get('back_home')
		if(go_home == ("Back")):
			show_feed = False
			context = {'username': request.user.username, 
			'channels': channels,'show': show_feed, 'events': future_events, 'notificationList': notificationList,
			'article_urls': article_urls, 'article_images': article_images, "controlled_channels": request.user.controlledChannels}

		else:
			c_name = None
			channel = None
			
			# Handle post request when a channel's event is being added to the user's events
			# or the user is unsubscribing
			for key in request.POST:
				split = key.split('-')
				print split[0]
				if len(split) == 2: 
					if split[0].isdigit():
						c_name = split[1]
						channel = get_object_or_404(Channel, name=c_name)
						
						if channel.events.filter(pk = split[0]).exists() and request.user.channel_set.filter(name=c_name).exists():
							event = channel.events.filter(pk = split[0]).first()
							request.user.events.add(event)
							
					if split[0] == "Unsubscribe":
						c_name = split[1]
						channel = get_object_or_404(Channel, name=c_name)
						channel.subscribers.remove(request.user)
						show_feed = False
						channels = request.user.channel_set.order_by("name").all()
						context = {'username': request.user.username, 
						'channels': channels,'show': show_feed, 'events': events, 'notificationList': notificationList}
						return render(request, 'jam/index/index_landing_home.html', context)
					
			
			if channel == None:
				c_name = form_data.get('channel_name')
				channel = get_object_or_404(Channel, name=c_name)			
					
			is_admin = False
			if request.user.controlledChannels.filter(name=channel.name).exists():
				is_admin = True
			
			
			
			for e in channel.events.all():
				if (e.event_date <= datetime.now().date()):
					if (e.event_date == datetime.now().date()) and (e.start_time >= datetime.now().time()):
						continue #if the event already happened today, don't add it
					channel.events.remove(e)
			
			added_events = channel.events.all() & request.user.events.all()
			unadded_events = channel.events.all().exclude(pk__in = added_events.all())
			
			context = {'channel_name': channel.name, 'channel_nickname': channel.moniker,
				'channel_description': channel.description, 'channel_status': channel.is_public, 'notificationList': notificationList, 
				'is_admin': is_admin, 'username': request.user.username, 'channels': channels, 'show': show_feed, 
				"adminNotes": channel.adminNotes.order_by("-created_at"), 'unadded_e': unadded_events, 'added_e': added_events, 
				"controlled_channels": request.user.controlledChannels}
			

	return render(request, 'jam/index/index_landing_home.html', context)


@login_required
def profile(request):
	import pdb;
	user = User.objects.get(username = request.user.username)
	if user:
		try:
			profile = Profile.objects.get(user=request.user.username)
		except ObjectDoesNotExist:
			profile = None
	
	profile_edit = False 
	show_profile = True 

	form_data = request.POST
	
	if form_data:
		if('profile_edit' in form_data):
			profile_edit = True 
			show_profile = False 
			print "in profile edit in data" 

		elif profile: #already contained in DB, want to edit
			
			name_input = form_data.get('name')
			if(name_input):
				names = name_input.split(' ')
				if len(names) > 1:
					first=names[0]
					last=names[1]
				else: 
					first = names[0]
					last = ''
			else:
				first = ''
				last = ''

			profile.first_name = first
			profile.last_name = last
			profile.email=form_data.get('user_email')
			profile.phone_number=form_data.get('user_phone_number')
			profile.address=form_data.get('user_address')
			profile.gender=form_data.get('gender')
			profile.grad_date=form_data.get('user_grad_date')
			profile.save()

		else:
			name_input = form_data.get('name')
			if(name_input):
				names = name_input.split(' ')
				if len(names) > 1:
					first=names[0]
					last=names[1]
				else: 
					first = names[0]
					last = ''
			else:
				first = ''
				last = ''
			profile = Profile(user=request.user.username,
							  first_name=first,
							  last_name=last,
							  email=form_data.get('user_email'),
							  phone_number=form_data.get('user_phone_number'),
							  address=form_data.get('user_address'),
							  gender=form_data.get('gender'),
							  grad_date=form_data.get('user_grad_date'),
							 )
			profile.save()
		# profile.save()
		# remember to cause profile to save again!!! 

		#return render(request, 'jam/index/index.html', {})
	'''
	profile_edit = False 
	show_profile = True 
	data = request.POST 
	if(data): 
		if ('profile_edit' in data): 
			profile_edit = True 
			show_profile = False 
			print "in profile edit in data" 
	'''
	context = {'show_profile' : show_profile, 'profile_edit': profile_edit, 'profile': profile, 'username': request.user.username}
	return render(request, 'jam/user/profile.html', context)


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
	return render(request, 'jam/user/manage_account.html', context)
