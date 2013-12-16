from django.conf.urls import patterns, url

from genomeassist.scheduler import views

urlpatterns = patterns('',
    url(r'^create/_container/$', views.create_aligner_container, name='create_aligner_container'),
    url(r'^create/(?P<aligner>\w+)/$', views.create_aligner, name='create_aligner'),
    url(r'^create/$', views.create, name='create'),
    url(r'^delete/(?P<pk>\d+)/$', views.delete, name='delete'),
    url(r'^undelete/(?P<pk>\d+)/$', views.undelete, name='undelete'),
    url(r'^view/(?P<pk>\d+)/$', views.detail, name='detail'),
    url(r'^view/$', views.index, name='index'),
    url(r'^$', views.home, name='home'),
)
