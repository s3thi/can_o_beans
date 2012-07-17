from gravy.models import Page
from django.db.models.signals import post_save
from journal.signals import clear_cache_on_save


class JournalEntry(Page):
    pass

post_save.connect(clear_cache_on_save, sender=JournalEntry)