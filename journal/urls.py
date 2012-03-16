from django.conf.urls.defaults import patterns, include, url
from journal.views import ArchiveView, EntryView

y = '(?P<year>\d{4})'
m = '(?P<month>\w+)'
d = '(?P<day>\d{1,2})'
s = '(?P<slug>\S+)'

urlpatterns = patterns('journal.views',
    url('^$', ArchiveView.as_view()),
    url('^{0}/$'.format(y), ArchiveView.as_view()),
    url('^{0}/{1}/$'.format(y, m), ArchiveView.as_view()),
    url('^{0}/{1}/{2}/$'.format(y, m, d), ArchiveView.as_view()),
    url('^{0}/{1}/{2}/{3}/$'.format(y, m, d, s), EntryView.as_view()),
)
