from django.conf.urls import patterns, url, include
from swingtime import views as swingtime
from jam import views as jamViews

urlpatterns = patterns('', 

    url(r'^$', views.index, name='index'),
    url(r'profile', views.profile, name='profile'),
    url(r'companies/', views.companies, name='companies'),
    url(r'calendar/', views.calendar, name='calendar'),
    url(r'new_contact/', views.new_contact, name='new_contact'),
    url(r'new_company/', views.new_company, name='new_company'),
    url(r'new_event/', views.new_event, name='new_event'),
	url(r'channels/create/', views.new_channel, name='new_channel'),
	url(r'^events/add/$', swingtime.add_event, name='swingtime-add-event'),
	(r'^swingtime/', include('swingtime.urls'))
)

