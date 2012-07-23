from gravy.models import Page
from django.db.models.signals import post_save
from gravy.signals import clear_cache_on_save


class JournalEntry(Page):
    class Meta:
    	verbose_name_plural = "journal entries"

post_save.connect(clear_cache_on_save, sender=JournalEntry)