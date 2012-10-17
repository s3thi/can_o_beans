import datetime
from calendar import month_abbr
from django.contrib.syndication.views import Feed

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from django.views.generic import DetailView, dates
from django.utils.timezone import get_default_timezone
from journal.models import JournalEntry


months = dict()
for k, v in enumerate(month_abbr):
    months[v] = k


class JournalIndexView(dates.ArchiveIndexView):
    queryset = JournalEntry.objects.filter(published=True)
    context_object_name = 'journal_entry_list'
    date_field = 'published_on'
    paginate_by = 10
    allow_empty = True
    template_name = 'journal/journal_index.html'


class EntryView(DetailView):
    model = JournalEntry
    context_object_name = 'journal_entry'
    template_name = 'journal/entry.html'

    def get_queryset(self):
        published_on_lower = datetime.datetime(
            year=int(self.kwargs['year']),
            month=months[self.kwargs['month']],
            day=int(self.kwargs['day']),
            hour=0,
            minute=0,
            second=0,
            tzinfo=get_default_timezone())

        published_on_upper = published_on_lower.replace(
            hour=23,
            minute=59,
            second=59
        )
            
        return JournalEntry.objects.filter(
            published_on__gte=published_on_lower,
            published_on__lte=published_on_upper,
            slug=self.kwargs['slug']
        )


class LatestEntriesFeed(Feed):
    title = 'Latest journal entries from AnkurSethi.in'
    link = '/journal/'
    author_name = 'Ankur Sethi'
    author_email = 'contact@ankursethi.in'

    def items(self):
        return JournalEntry.objects.filter(published=True).order_by('-published_on')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content_processed