from django.conf.urls.defaults import patterns, include, url
from journal.views import (JournalIndexView, ArchiveIndexView,  YearArchiveView,
                           MonthArchiveView, DayArchiveView, EntryView,
                           SlugEntryView, LatestEntriesFeed)

y = '(?P<year>\d{4})'
m = '(?P<month>\w+)'
d = '(?P<day>\d{1,2})'
s = '(?P<slug>\S+)'
k = '(?P<pk>\d+)'
p = '(?P<page>\d+)'

urlpatterns = patterns('',
    url('^$', JournalIndexView.as_view(),
        name='cob_journal_index'),
    url('^page/{0}/'.format(p), JournalIndexView.as_view(),
        name='cob_journal_index_paginated'),

    url('^archive/$', ArchiveIndexView.as_view(),
        name='cob_journal_archive_index'),
    url('^archive/{0}/$'.format(y), YearArchiveView.as_view(),
        name='cob_journal_year_archive_view'),
    url('^archive/{0}/{1}/$'.format(y, m), MonthArchiveView.as_view(),
        name='cob_journal_month_archive_view'),

    url('^{0}/{1}/{2}/{3}/$'.format(y, m, d, k), EntryView.as_view(),
        name='cob_journal_entry_detail_view_pk'),
    url('^{0}/{1}/{2}/{3}/$'.format(y, m, d, s), SlugEntryView.as_view(),
        name='cob_journal_entry_detail_view'),

    url(r'^feed/$', LatestEntriesFeed(), name='feed_view'),
)