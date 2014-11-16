from django.conf.urls import patterns, url, include
#from django.core.urlresolvers import reverse
from jam import views
from swingtime import views as swingtime

urlpatterns = patterns('', 
    url(r'^$', views.index, name='index'),
    url(r'^profile', views.profile, name='profile'),
    url(r'^companies/(?P<company_name>.+)/$', views.companies, name='companies'),
    url(r'^contacts/', views.contacts, name='contacts'),
    url(r'^cal/', views.cal, name='cal'),
    url(r'^new_contact/', views.new_contact, name='new_contact'),
    url(r'^new_company/', views.new_company, name='new_company'),
    url(r'^company/(?P<company_name>.+)/$', views.company_page, name='company_page'),
    url(r'^edit/company/(?P<company_name>.+)/$', views.edit_company, name='edit_company'),

    url(r'^new_event/', views.new_event, name='new_event'),
    #url(r'companies/export_companies/', views.export_companies, name='export_companies'),
	url(r'^channels/create/', views.new_channel, name='new_channel'),
    url(r'^channels/activate/(?P<channel_name>.+)/(?P<user_name>.+)/$', views.activate_subscriber, name='activate_subscriber'),
	url(r'^channels/view/(?P<channel_name>.+)/$', views.view_channel, name="view_channel"),
	url(r'^channels/view_as_admin/(?P<channel_name>.+)/$', views.view_channel_as_admin, name="view_channel_as_admin"),

    #url(r'^events/monthly/$', swingtime.month_view, name='swingtime-monthly-view'),
    url(r'^account_management', views.manage_account, name='manage_account'),
    url(r'^channels/list', views.channel_list, name='channel_list'),

##########################################################################################################################
# from django-swingtime https://github.com/dakrauth/django-swingtime/ 
# instead of importing urls we added them manually to allow for user specific calendars
# any url that uses view. instead of swingtime. has a modifed view in our views.py
##########################################################################################################################
    # url(
    #     r'^(?:calendar/)?$', 
    #     swingtime.today_view, 
    #     name='swingtime-today'
    # ),

    url(
        r'^calendar/(?P<year>\d{4})/$', 
        views.year_view, 
        name='swingtime-yearly-view'
    ),

    url(
        r'^calendar/(\d{4})/(0?[1-9]|1[012])/$', 
        views.month_view, 
        name='swingtime-monthly-view'
    ),

    url(
        r'^calendar/(\d{4})/(0?[1-9]|1[012])/([0-3]?\d)/$', 
        swingtime.day_view, 
        name='swingtime-daily-view'
    ),

    url(
        r'^events/$',
        views.event_listing,
        name='swingtime-events'
    ),
        
    url(
        r'^events/add/(?P<channel_name>.+)/$', 
        views.add_event, 
        name='swingtime-add-event'
    ),
	
	url(
        r'^events/add/$', 
        views.add_event, 
        name='swingtime-add-event'
    ),
    
    url(
        r'^events/(\d+)/$', 
        views.event_view, 
        name='swingtime-event'
    ),
    
    url(
        r'^events/(\d+)/(\d+)/$', 
        views.occurrence_view, 
        name='swingtime-occurrence'
    ),
)

##########################################################################################################################################
# END TO SWINGTIME URLS
##########################################################################################################################################
