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

from jam.models import Contact, Company, Event, Profile, Channel
from django.http import HttpResponseRedirect

from swingtime import utils, forms


# Create your views here.
@login_required
def index(request):
    context = {'username': request.user.username}
    if request.method == "GET":
		form = UploadFileForm()
		context = {'username': request.user.username, 'form': form}
    return render(request, 'jam/index_homepage.html', context)

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
		channel = Channel(name=form_data.get('name'), moniker=form_data.get('moniker'), description=form_data.get('description'), is_public=(form_data.get('is_public')))
		print form_data.get('is_public')
		channel.save()
		channel.subscribers.add(request.user)
		channel.admins.add(request.user)

		return HttpResponseRedirect("/jam/")

	else:
		return render(request, 'jam/new_channel.html')

def new_contact(request):
	form_data = request.POST
	contact = Contact(name=form_data.get('name'),
					  phone_number=form_data.get('phone'),
					  email=form_data.get('email'),
					  employer=form_data.get('company'),
					  user=request.user.username)
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
	context = {'channel_name': channel.name, 'username': user_name, 'valid': is_admin}
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
			if user is not None and (user.controlledChannels.filter(name=channel_name).exists() == False or user == request.user):
				channel.subscribers.remove(User.objects.filter(username=key).first())

		if 'nickname' in request.POST:
			channel.moniker = request.POST.get('nickname')
		if 'description' in request.POST:
			channel.description = request.POST.get('description')
		channel.save()

		return HttpResponseRedirect("/jam/channels/view_as_admin/" + channel.name)

	context = {'channel_name': channel.name, 'channel_nickname': channel.moniker,
		'channel_description': channel.description, 'channel_status': channel.is_public,
		'is_admin': is_admin, 'subscribers': channel.subscribers}

	return render(request, 'jam/view_channel_as_admin.html', context)


def new_company(request):
	if request.method == "POST" and request.FILES:
		form = UploadFileForm(request.FILES)
		read_from_file(request.user.username, request.FILES['filep'])
	if request.method == "POST":
		form_data = request.POST
		company = Company(name=form_data.get('name'),
						  application_deadline=form_data.get('deadline'),
						  user=request.user.username)
		company.save()
	context = {'username': request.user.username}
	return render(request, 'jam/index_homepage.html', context)

def new_event(request):
	form_data = request.POST
	event = Event(name=form_data.get('name'),
					  date=form_data.get('date'))
	event.save()
	return HttpResponse()

def companies(request):
	companies = Company.objects.filter(user=request.user.username)
	for company in companies:
		print company
	context = {'companies': companies}
	#context = {}
	return render(request, 'jam/companies.html', context)

def contacts(request):
	# contacts = Contacts.objects.filter(user=request.user.username)
	# for contact in contacts:
	# 	print contact
	context = {'contact': contacts}
	#context = {}
	return render(request, 'jam/contacts.html', context)

def cal(request):
	context = {}
	return render(request, 'jam/calendar.html', context)

def channel_list(request):
	channels = Channel.objects.all()
	context={'channels': channels}
	return render(request,'jam/channel_list.html',context)
def test(request):
	context = {}
	return render(request, 'jam/base_companies.html', context)
