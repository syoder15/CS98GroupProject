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

def channel_list(request):
	form_data = request.POST
	channel_categories =  ChannelCategory.objects.all().order_by('-count')[:10]

	sub_channels = request.user.channel_set.all()

	# get channels in order of creation, starting with the most recent 
	channels = Channel.objects.order_by('-added').all()

	error = ''
	if(form_data):
		if 'search_category' in form_data:
			cat = form_data.get('search_category')
		elif 'search' in form_data:
			cat = form_data.get('search')
		# it must be a call from modal_add_channel to create a new channel!
		else: 
			cat =''
			new_channel(request) 
		
		# if no channels are categorized under a given search term, the channels returned are an empty list... 
		# the HTML will populate with the line "No results found" d
		
		if(cat != '' and ChannelCategory.objects.filter(name=cat).exists()):
			channels = {}
			channel_category = ChannelCategory.objects.get(name = cat)

			all_channels = Channel.objects.order_by('-added').all()
			all_sub_channels = request.user.channel_set.all()
			channels = []
			sub_channels = []

			# show only channels that contain searched category 
			for c in all_channels:
				if channel_category in c.categories.all():
					channels.append(c)
					if c in all_sub_channels:
						sub_channels.append(c)
			channel_categories = []
			channel_categories.append(channel_category)
		
	context={'channels': channels, 'sub_channels': sub_channels, 'categories': channel_categories, 'username': request.user.username, 'upload_form': upload_form}
	return render(request,'jam/channels/channel_list.html',context)


@login_required
def new_channel(request):
	if request.method == 'POST':
		print "GOT HERE TO NEW CHANNEL VIEW"
		form_data = request.POST

		if form_data.get('name') != "" and not Channel.objects.filter(name=form_data.get('name')).exists():
			category_names = form_data.get('category_names')
			channel = Channel(name=form_data.get('name'), 
				moniker=form_data.get('moniker'), 
				description=form_data.get('description'), 
				is_public=(form_data.get('is_public')))
			channel.save()
			for c in category_names.split(","):
				cat = None
				c = c.strip(' \t\n\r')
				if (ChannelCategory.objects.filter(name = c).exists()):
					cat = ChannelCategory.objects.get(name = c)
					cat.count += 1
				else:
					cat = ChannelCategory(name = c, count = 1)
				cat.save()
				cat.save()
				channel.categories.add(cat)
			channel.subscribers.add(request.user)
			channel.admins.add(request.user)
			channel.save()
			return HttpResponseRedirect("/jam/")
		else:
			errors = ""
			if Channel.objects.filter(name=form_data.get('name')).exists():
				errors = "A channel with that name already exists: please choose another."
			context = {"errors": errors}
			
			response={}
			response["error"] = errors
			return HttpResponseBadRequest(json.dumps(response),content_type="application/json")
			#return render(request, 'jam/channels/new_channel.html', context)

	else:
		cats = ChannelCategory.objects.all()
		context = {'categories':cats}
		return render(request, 'jam/channels/new_channel.html', context)

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

	context = {'channel_name': channel.name, 'channel_nickname': channel.moniker, 'events': channel.events,
		'channel_description': channel.description, 'channel_status': channel.is_public,
		'is_admin': is_admin, 'subscribers': channel.subscribers, 'adminNotes': channel.adminNotes.order_by("-created_at"), 'username': request.user.username}


	return render(request, 'jam/channels/view_channel_as_admin.html', context)

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
	return render(request, 'jam/channels/activate_subscriber.html', context)


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

	added_events = channel.events.all() & request.user.profile.events.all()
	unadded_events = channel.events.all().exclude(pk__in = added_events.all())
		
	context = {'channel_name': channel.name, 'channel_nickname': channel.moniker,
		'channel_description': channel.description, 'channel_status': channel.is_public, 'categories': channel.categories.all(), 'is_subscriber': is_subscriber,
		'is_admin': is_admin, 'unadded_e': unadded_events, 'added_e': added_events}

	if request.method == 'POST':
		event_added = False
		for key in request.POST:
			if key.isdigit() and channel.events.filter(pk = key).exists():
				event = channel.events.filter(pk = key).first()
				request.user.profile.events.add(event)
				event_added = True
		
		if 'Unsubscribe' in request.POST:
			channel.subscribers.remove(request.user)
		elif channel.is_public and 'Subscribe' in request.POST:
			channel.subscribers.add(request.user)
		elif not event_added:
			site = settings.DOMAIN
			link = site + "/jam/channels/activate/" + channel.name + "/" + request.user.username
			for admin in channel.admins.all():
				subject = channel.name + " Suscriber request!"
				body = request.user.username + " would like to join your channel! Click this link to let them in :)\n" + link
				send_mail(subject,body,'dartmouthjam@gmail.com', [admin.email], fail_silently=False)
		return HttpResponseRedirect("/jam/channels/view/" + channel.name)

	return render(request, 'jam/channels/view_channel.html', context)

