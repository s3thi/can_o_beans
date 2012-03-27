from django.conf.urls.defaults import patterns, include, url
from journal.views import (ArchiveIndexView,  YearArchiveView,
                           MonthArchiveView, DayArchiveView, EntryView,
                           SlugEntryView)

y = '(?P<year>\d{4})'
m = '(?P<month>\w+)'
d = '(?P<day>\d{1,2})'
s = '(?P<slug>\S+)'
k = '(?P<pk>\d+)'

urlpatterns = patterns('',
    url('^$', ArchiveIndexView.as_view()),
    url('^{0}/$'.format(y), YearArchiveView.as_view()),
    url('^{0}/{1}/$'.format(y, m), MonthArchiveView.as_view()),
    url('^{0}/{1}/{2}/$'.format(y, m, d), DayArchiveView.as_view()),
    url('^{0}/{1}/{2}/{3}/$'.format(y, m, d, k), EntryView.as_view(),
        name='entry-detail-view-pk'),
    url('^{0}/{1}/{2}/{3}/$'.format(y, m, d, s), SlugEntryView.as_view(),
        name='entry-detail-view')
)
