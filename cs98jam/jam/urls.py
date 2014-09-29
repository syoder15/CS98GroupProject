from django.conf.urls import patterns, url

from jam import views

urlpatterns = patterns('', 
    url(r'^$', views.index, name='index'),
    url(r'profile', views.profile, name='profile'),
    url(r'new_contact/', views.new_contact, name='new_contact')), 
	url(r'companies/', views.companies, name='companies'))
