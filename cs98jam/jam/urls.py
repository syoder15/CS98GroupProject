from django.conf.urls import patterns, url, include
from django.core.urlresolvers import reverse
from swingtime import views as swingtime
from jam import views as jamViews

urlpatterns = patterns('', 
    url(r'^$', jamViews.index, name='index'),
    url(r'profile', jamViews.profile, name='profile'),
    url(r'companies/', jamViews.companies, name='companies'),
    url(r'calendar/', jamViews.calendar, name='calendar'),
    url(r'new_contact/', jamViews.new_contact, name='new_contact'),
    url(r'new_company/', jamViews.new_company, name='new_company'),
    url(r'new_event/', jamViews.new_event, name='new_event'),
    (r'^swingtime/', include('swingtime.urls')),
)
