from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from swingtime.models import Event as SwingtimeEvent


# Create your models here.
class Company(models.Model):
    
    def __unicode__(self):
        return self.name
 	class Meta:
 		verbose_name_plural =_('Companies')
    name = models.CharField(max_length=50)
    user = models.CharField(max_length=20)
    application_deadline = models.DateField()

class Contact(models.Model):

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=50)
    phone_number = models.IntegerField(default=0)
    email = models.CharField(max_length=50)
    employer = models.CharField(max_length=50)
    user = models.CharField(max_length=20)


# class Event(models.Model):

#     def __unicode__(self):
#         return self.name

#     name = models.CharField(max_length=50)
#     date = models.DateField()

class Channel(models.Model): 
	def __unicode__(self):
		return self.name
		
	name = models.CharField(max_length = 50)
	moniker = models.CharField(max_length = 20)
	description = models.CharField(max_length = 140)
	is_public = models.BooleanField(default=False)
	subscribers = models.ManyToManyField(User, blank=True, null=True)
	admins = models.ManyToManyField(User, related_name="controlledChannels", blank=True, null=True)
	
	
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
	phone_number = models.IntegerField(default=0, blank=True)
	address = models.CharField(max_length=50, blank=True)
	city = models.CharField(max_length=40, blank=True)
	state = models.CharField(max_length=13, blank=True)
	zip_code = models.CharField(max_length=6, blank=True)

	#An error may occur here, unsure as to what rep of radiobutton is
	gender = models.CharField(max_length=10, blank=True)

	school = models.CharField(max_length=50, blank=True)

	grad_month = models.CharField(max_length=10, blank=True)
	grad_year = models.IntegerField(default=0, blank=True)

class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name="profile")
	activation_key = models.CharField(max_length=40)
	key_expires = models.DateTimeField()
	events = models.ManyToManyField(SwingtimeEvent)
	# notification freq, defined as how many emails sent per week
	# 42 means 4-hour feed, 7 means daily digest, and 1 means week in review 
	notification_frequency = models.IntegerField(default=0)
