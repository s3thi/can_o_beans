from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from journal.models import JournalEntry

months = [ '', 'january', 'february', 'march', 'april', 'may', 'june', 'july',
           'august', 'september', 'october', 'november', 'december' ]

class ArchiveView(ListView):

    context_object_name = 'journal_entry_list'
    template_name = 'journal/archive.html'

    def get_queryset(self):
        qs = JournalEntry.objects.all()

        has_year = 'year' in self.kwargs
        has_month = 'month' in self.kwargs
        has_day = 'day' in self.kwargs

        if has_year:
            qs = qs.filter(
                published_on__year=self.kwargs['year']
            )

        if has_year and has_month:
            qs = qs.filter(
                published_on__month=to_numeric_month(self.kwargs['month'])
            )

        if has_year and has_month and has_day:
            qs = qs.filter(
                published_on__day=self.kwargs['day']
            )

        return qs


class EntryView(DetailView):

    model = JournalEntry
    context_object_name = 'journal_entry'
    template_name = 'journal/entry.html'


def to_numeric_month(month):
    try:
        return int(month)
    except ValueError:
        return months.index(month)
