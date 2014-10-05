from django.conf.urls import patterns, include, url

from django.contrib import admin
from cs98jam.views import *

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
	
	url(r'^password_change/reset/$', 
        'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/password_change/done/'},
        name="password_reset"),
		
		 (r'^password_change/done/$',
        'django.contrib.auth.views.password_reset_done'),
		
		(r'^password_change/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : '/password_change/complete/'}),
		
		(r'^password_change/complete/$', 
        'django.contrib.auth.views.password_reset_complete'),
)
