from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/$', 'django.contrib.auth.views.login', {'redirect_field_name': '/'},
        name='auth_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login',
        name='auth_logout'),

    url(r'^journal/', include('journal.urls')),
)

urlpatterns += staticfiles_urlpatterns()
