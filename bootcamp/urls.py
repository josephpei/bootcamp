from django.conf.urls import patterns, include, url

from core import views as core_views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from authentication import views as bootcamp_auth_views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bootcamp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', core_views.home, name='home'),
    url(r'^login', auth_views.login, {'template_name': 'core/cover.html'}, name='login'),
    url(r'^logout', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^profile', core_views.profile, name='profile'),
    url(r'^settings/$', core_views.settings, name='settings'),
    url(r'^settings/picture/$', core_views.picture, name='picture'),
    url(r'^settings/upload_picture/$', core_views.upload_picture, name='upload_picture'),
    url(r'settings/save_uploaded_picture/$', core_views.save_uploaded_picture, name='save_uploaded_picture'),
    url(r'settings/password/$', core_views.password, name='password'),
    # url(r'accounts/profile', core_views.profile, name='user_profile'),
    # url(r'accounts/profile', TemplateView.as_view(template_name='core/profile.html'), name='user_profile'),
    url(r'^signup/$', bootcamp_auth_views.signup, name='signup'),
    url(r'^feeds/', include('feeds.urls')),
    url(r'^articles/', include('articles.urls')),
    url(r'^questions/', include('questions.urls')),
    url(r'^(?P<username>[^/]+)/$', core_views.profile, name='profile')
)
