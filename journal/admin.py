from journal.models import JournalEntry
from django.contrib import admin

class JournalEntryAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'author', 'published_on', 'published']
    list_display = ('title', 'published_on')
    list_filter = ['published_on']
    search_fields = ['title']
    date_hierarchy = 'published_on'

admin.site.register(JournalEntry, JournalEntryAdmin)
