from django.conf.urls.defaults import patterns, include, url
from journal.views import JournalEntryListView

y = '(?P<year>\d{4})'
m = '(?P<month>\w+)'
d = '(?P<day>\d{1,2})'
s = '(?P<slug>\S+)'

urlpatterns = patterns('journal.views',
    url('^$', JournalEntryListView.as_view()),
    url('^{0}/$'.format(y), JournalEntryListView.as_view()),
    url('^{0}/{1}/$'.format(y, m), JournalEntryListView.as_view()),
    url('^{0}/{1}/{2}/$'.format(y, m, d), JournalEntryListView.as_view()),
    url('^{0}/{1}/{2}/{3}/$'.format(y, m, d, s), 'show_entry'),
)
