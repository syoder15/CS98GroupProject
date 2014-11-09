from django.contrib import admin
from jam.models import Company, Contact, Profile, Channel, UserProfile, ChannelAdminNote, ChannelCategory

# Register your models here.
admin.site.register(Company)
admin.site.register(Contact)
#admin.site.register(Event)
admin.site.register(Profile)
admin.site.register(Channel)
admin.site.register(UserProfile)
admin.site.register(ChannelAdminNote)
admin.site.register(ChannelCategory)