import datetime
from django.contrib.syndication.views import Feed
from django.views.generic import DetailView, dates
from django.utils.timezone import get_default_timezone
from journal.models import JournalEntry
from gravy.utils import StaffMemberRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from journal.forms import JournalEntryForm
from django.core.urlresolvers import reverse


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
        from calendar import month_abbr
        months = dict()
        for k, v in enumerate(month_abbr):
            months[v] = k
        
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


class CreateJournalEntryView(StaffMemberRequiredMixin, CreateView):
    model = JournalEntry
    template_name = 'journal/journal_new.html'
    form_class = JournalEntryForm

    def get_success_url(self):
        return reverse('journal_entry_edit', kwargs={'pk': self.object.id})

    def get_form(self, *args, **kwargs):
        return self.form_class('journal_entry_new', **self.get_form_kwargs())


class EditJournalEntryView(StaffMemberRequiredMixin, UpdateView):
        model = JournalEntry
        template_name = 'journal/journal_edit.html'
        form_class = JournalEntryForm
        context_object_name = 'entry'

        def get_success_url(self):
            return reverse('journal_entry_edit', kwargs={'pk': self.object.id})

        def get_form(self, *args, **kwargs):
            return self.form_class(
                reverse('journal_entry_edit', kwargs={'pk': self.object.id}),
                **self.get_form_kwargs()
            )
