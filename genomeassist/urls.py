from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login

import genomeassist.scheduler.urls
from .scheduler.forms import login_helper

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login, {'extra_context': {'helper': login_helper}}, name='login'),
    url(r'^accounts/logout/$', logout_then_login, name='logout'),
    url(r'', include(genomeassist.scheduler.urls, namespace='scheduler')),
)
