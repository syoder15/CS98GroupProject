from django.contrib import admin
from jam.models import Company, Contact, Event, Profile, Channel, UserProfile


# Register your models here.
admin.site.register(Company)
admin.site.register(Contact)
admin.site.register(Event)
admin.site.register(Profile)
admin.site.register(Channel)
admin.site.register(UserProfile)
