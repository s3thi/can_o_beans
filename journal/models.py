from django.db import models
from django.contrib.auth.models import User

'''
Okay, so this is how things work around here: when you go to /y/, you find the
archive for one whole year, and likewise for /y/m/ and /y/m/d/. To go to
a specific entry, you need to enter a URL of the form /y/m/d/title-of-entry/.

The string 'title-of-entry' in the URL above is called a slug. Each entry made
on a single day must have a unique slug. If the slug is missing,
Can 'o Beans will automatically try to create one using the title of the entry.
For example, an entry titled "I Don't Like These New Bamboo Mats" will have
"i-dont-like-these-new-bamboo-mats" as its slug.

If both the slug and the title for an entry are missing, Can 'o Beans will
use the first 256 characters of the entry to generate a slug.

If this a slug is not unique, Can 'o Beans will eat a few characters off
the end of the slug to make room for a unique numeric identifier. First, a  "-1"
will be appended to the end of the slug. If the new slug is still not unique, the
"-1" will be incremented to "-2", and so on until a unique slug has been found.
'''

class JournalEntry(models.Model):
    title = models.TextField(blank=True, null=True)
    slug = models.CharField(max_length=256, blank=True)
    published_on = models.DateTimeField()
    content = models.TextField()
    author = models.ForeignKey(User)

    def __unicode__(self):
        if self.title:
            return '<{0}>'.format(self.title)
        else:
            return '<{0}>'.format(self.slug)
