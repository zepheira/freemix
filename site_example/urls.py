from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
#    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'accounts/login.html'},
        name='acct_login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login',
        name='acct_logout'),
    url(r'^data/', include('freemix.dataset.urls')),
    (r'^search/', include('haystack.urls')),

)
