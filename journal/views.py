import datetime
from calendar import month_abbr

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

class ArchiveViewMixin(object):

    queryset = JournalEntry.objects.filter(published=True)
    context_object_name = 'journal_entry_list'
    template_name = 'journal/base.html'
    date_field = 'published_on'


class JournalIndexView(ArchiveViewMixin, dates.ArchiveIndexView):
    
    template_name = 'journal/journal_index.html'
    paginate_by = 10
    allow_empty = True


class ArchiveIndexView(ArchiveViewMixin, dates.ArchiveIndexView):

    template_name = 'journal/archive_full.html'


class YearArchiveView(ArchiveViewMixin, dates.YearArchiveView):
    
    template_name = 'journal/archive_year.html'
    make_object_list = True


class MonthArchiveView(ArchiveViewMixin, dates.MonthArchiveView):

    template_name = 'journal/archive_month.html'


class DayArchiveView(ArchiveViewMixin, dates.DayArchiveView):

    pass


class EntryView(DetailView):

    model = JournalEntry
    context_object_name = 'journal_entry'
    template_name = 'journal/entry.html'


class SlugEntryView(EntryView):

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
