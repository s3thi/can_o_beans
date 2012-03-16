from django.http import HttpResponse
from django.views.generic import ListView
from journal.models import JournalEntry

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

def show_entry(request, year, month, day, title):
	return HttpResponse('showing a post')
