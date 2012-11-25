from django.conf.urls.defaults import patterns, include, url
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from journal.models import JournalEntry

from django.contrib import admin
admin.autodiscover()


journal_sitemap_info_dict = {
    'queryset': JournalEntry.objects.filter(published=True),
    'date_field': 'published_on'
}


sitemaps = {
    'flatpages': FlatPageSitemap,
    'journal': GenericSitemap(journal_sitemap_info_dict)
}


urlpatterns = patterns('',
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^journal/', include('journal.urls')),
    url(r'^bookmarks/', include('bookmarks.urls')),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)

urlpatterns += staticfiles_urlpatterns()
