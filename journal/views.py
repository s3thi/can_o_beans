from django.views.generic import DetailView, dates
from journal.models import JournalEntry


class ArchiveViewMixin(object):

    model = JournalEntry
    context_object_name = 'journal_entry_list'
    template_name = 'journal/archive.html'
    date_field = 'published_on'


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
