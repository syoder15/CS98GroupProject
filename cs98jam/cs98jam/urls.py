from django.conf.urls import patterns, include, url
from cs98jam.views import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cs98jam.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^$', main_page),
	
    url(r'^admin/', include(admin.site.urls)),
    url(r'^jam/', include('jam.urls')),
	
	# Login / logout.
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', logout_page),
	(r'^register/$', register),
    (r'^activate/$', activate), 
)
