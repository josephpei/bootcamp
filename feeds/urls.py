from django.conf.urls import patterns, include, url
import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.feeds, name='feeds'),
    url(r'post/$', views.post, name='post'),
    url(r'like/$', views.like, name='like')
)
