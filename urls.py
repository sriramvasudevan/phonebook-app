from django.conf.urls.defaults import patterns, include, url
from phsite.views import *
#from django.contrib.auth.views import login, logout
from phsite.registration import login, logout


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$',login),
    (r'^home/logout/$', logout),
    (r'^home/edit/(\d+)/$', edit_contact),
    (r'^home/delete/(\d+)/$', del_contact),
    (r'^home/search/$', search_contact),
    (r'^register/$', register),
    (r'^home/$', home),
    (r'^home/add/$', add_contact),
    # Examples:
    # url(r'^$', 'phsite.views.home', name='home'),
    # url(r'^phsite/', include('phsite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
