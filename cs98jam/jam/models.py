from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from swingtime.models import Event as SwingtimeEvent



class Event(models.Model):

	def __unicode__(self):
		return self.name

	name = models.CharField(max_length=50)
	description = models.CharField(max_length=150)
	companies = models.CharField(max_length=200, default='')
	event_type = models.CharField(max_length=5)
	event_date = models.DateField()
	start_time = models.TimeField()
	end_time = models.TimeField()
	creator = models.ForeignKey(User, related_name="owned_events", blank=True)
	users = models.ManyToManyField(User, related_name="events", blank=True)

class Company(models.Model):
    
    def __unicode__(self):
        return self.name
 	class Meta:
 		verbose_name_plural =_('Companies')
    name = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    user = models.ForeignKey(User)
    application_deadline = models.DateField(blank=True, null=True)
    application_status = models.BooleanField(default=False)
    events = models.ManyToManyField(Event, blank=True, related_name="company_events")
    link = models.CharField(max_length=150, blank=True)

class Contact(models.Model):

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=50)
    phone_number = models.IntegerField(default=0,blank=True,null=True)
    email = models.CharField(max_length=50,blank=True,null=True)
    employer = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    user = models.ForeignKey(User)


class ChannelCategory(models.Model):
	def __unicode__(self):
		return self.name
	name = models.CharField(max_length = 50)
	count = models.IntegerField(default=0, blank=True)

class Channel(models.Model): 
	def __unicode__(self):
		return self.name
		
	name = models.CharField(max_length = 50)
	moniker = models.CharField(max_length = 20)
	description = models.CharField(max_length = 140)
	is_public = models.BooleanField(default=False)
	subscribers = models.ManyToManyField(User, blank=True, null=True)
	admins = models.ManyToManyField(User, related_name="controlledChannels", blank=True, null=True)
	events = models.ManyToManyField(Event, blank=True)
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	categories = models.ManyToManyField(ChannelCategory, related_name="channelCategories", blank=True, null=True)

class ChannelAdminNote(models.Model):
	def __unicode__(self):
		return self.text
	created_at = models.DateTimeField(default=timezone.now)
	home_channel = models.ForeignKey(Channel, related_name="adminNotes")
	text = models.CharField(max_length = 1000)
	author =  models.ForeignKey(User)


class Profile(models.Model):
	def __unicode__(self):
		return self.first_name

	user = models.CharField(max_length=20)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=50)
	email = models.EmailField(max_length=60)
	phone_number = models.CharField(max_length=11, blank=True)
	address = models.CharField(max_length=50, blank=True)
	city = models.CharField(max_length=40, blank=True)
	state = models.CharField(max_length=13, blank=True)
	zip_code = models.CharField(max_length=6, blank=True)

	#An error may occur here, unsure as to what rep of radiobutton is
	gender = models.CharField(max_length=10, blank=True)

	school = models.CharField(max_length=50, blank=True)

	grad_date = models.CharField(max_length=15, blank=True)
	#grad_year = models.IntegerField(default=0, blank=True)
	
class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name="profile")
	activation_key = models.CharField(max_length=40)
	key_expires = models.DateTimeField()
	events = models.ManyToManyField(Event, blank=True)
	owned_events = models.ManyToManyField(Event, blank=True, related_name="owned_events") 
	# notification freq, defined as how many emails sent per week
	# 42 means 4-hour feed, 7 means daily digest, and 1 means week in review 
	notification_frequency = models.IntegerField(default=0)
