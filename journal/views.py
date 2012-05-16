import datetime
from calendar import month_abbr
from collections import OrderedDict
from django.views.generic import DetailView, dates
from django.utils.timezone import get_default_timezone
from journal.models import JournalEntry


months = { v: k for k, v in enumerate(month_abbr) }


class ArchiveViewMixin(object):

    model = JournalEntry
    context_object_name = 'journal_entry_list'
    template_name = 'journal/archive.html'
    date_field = 'published_on'

    def get_context_data(self, **kwargs):
        context = super(ArchiveViewMixin, self).get_context_data(**kwargs)
        context['active_years'] = self.get_active_years()
        for year in context['active_years'].keys():
            context['active_years'][year] = self.get_active_months(year)
        
        return context

    def get_active_years(self):
        # TODO: find a more efficient method for doing this lookup.
        # SQLite doesn't seem to support DISTINCT, so the distinct() function
        # on QuerySets doesn't work.
        active_years = { je.published_on.year : None for je in
                 JournalEntry.objects.all() }
        return OrderedDict(sorted(active_years.items(), key=lambda k: k[0]))

    def get_active_months(self, year):
        return { je.published_on.month for je in
                 JournalEntry.objects.filter(published_on__year=year) }


class ArchiveIndexView(ArchiveViewMixin, dates.ArchiveIndexView):

    pass


class YearArchiveView(ArchiveViewMixin, dates.YearArchiveView):

    make_object_list = True


class MonthArchiveView(ArchiveViewMixin, dates.MonthArchiveView):

    pass


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
