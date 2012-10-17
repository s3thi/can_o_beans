from django.conf.urls.defaults import patterns, include, url
from journal import views

y = '(?P<year>\d{4})'
m = '(?P<month>\w+)'
d = '(?P<day>\d{1,2})'
s = '(?P<slug>\S+)'
k = '(?P<pk>\d+)'
p = '(?P<page>\d+)'

urlpatterns = patterns('',
    url('^$', views.JournalIndexView.as_view(),
        name='cob_journal_index'),
    url('^page/{0}/'.format(p), views.JournalIndexView.as_view(),
        name='cob_journal_index_paginated'),

    url('^{0}/{1}/{2}/{3}/$'.format(y, m, d, s), views.EntryView.as_view(),
        name='cob_journal_entry_detail_view'),

    url(r'^feed/$', views.LatestEntriesFeed(), name='feed_view'),
)