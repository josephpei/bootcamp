from django.conf.urls import patterns, include, url
import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.articles, name='articles'),
    url(r'^write/$', views.write, name='write'),
    url(r'^preview/$', views.preview, name='preview'),
    url(r'^drafts/$', views.drafts, name='drafts'),
    url(r'^edit/(?P<id>\d+)/$', views.edit, name='edit_article'),
    url(r'^(?P<slug>[-\w]+)/$', views.article, name='article')
)