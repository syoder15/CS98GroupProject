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
	events = request.user.profile.events.order_by("occurrence").all()
	future_events = []
	for e in events:
		for u in e.upcoming_occurrences():
			if u.start_time >= timezone.now():
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
			'channels': channels, 'show': show_feed ,'events': events, 'notificationList': notificationList, 'app_list': app_notifications,
			'article_urls': article_urls, 'article_images': article_images}

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
			'channels': channels,'show': show_feed, 'events': events, 'notificationList': notificationList,
			'article_urls': article_urls, 'article_images': article_images}

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
							request.user.profile.events.add(event)
							
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
			
			added_events = channel.events.all() & request.user.profile.events.all()
			unadded_events = channel.events.all().exclude(pk__in = added_events.all())
			
			context = {'channel_name': channel.name, 'channel_nickname': channel.moniker,
				'channel_description': channel.description, 'channel_status': channel.is_public, 'notificationList': notificationList, 
				'is_admin': is_admin, 'username': request.user.username, 'channels': channels, 'show': show_feed, 
				"adminNotes": channel.adminNotes.order_by("-created_at"), 'unadded_e': unadded_events, 'added_e': added_events}
			

	return render(request, 'jam/index/index_landing_home.html', context)


@login_required
def profile(request):
	import pdb;
	form_data = request.POST

	username = request.user.username
	#pdb.set_trace()
	#user = User.objects.get(username=username.lower())
	user = User.objects.get(username = username)
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

		#return render(request, 'jam/index/index.html', {})

	context = {'profile': profile, 'username': request.user.username}
	return render(request, 'jam/user/profile.html', context)