from django.db import models, IntegrityError
from django.db.models.signals import post_save
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.conf import settings
import pytz
from gravy.signals import clear_cache_on_save


# First, deal with flatpages and caching. Apparently, this is the best place
# to do that.
post_save.connect(clear_cache_on_save, sender=FlatPage)


''' Okay, so this is how things work around here: when you go to /y/,
you find the archive for one whole year, and likewise for /y/m/ and
/y/m/d/. To go to a specific entry, you need to enter a URL of the
form /y/m/d/title-of-entry/.

The string 'title-of-entry' in the URL above is called a slug. Each
entry made on a single day must have a unique slug. If the slug is
missing, Can 'o Beans will automatically try to create one using the
title of the entry.  For example, an entry titled "I Don't Like These
New Bamboo Mats" will have "i-dont-like-these-new-bamboo-mats" as its
slug.

If this slug is not unique, Can 'o Beans will eat a few characters
off the end of the slug to make room for a unique numeric
identifier. First, a "-1" will be appended to the end of the slug. If
the new slug is still not unique, the "-1" will be incremented to
"-2", and so on until a unique slug has been found.  '''


SLUG_MAXLEN = 256


class Page(models.Model):

    title = models.TextField()
    slug = models.SlugField(max_length=SLUG_MAXLEN, blank=True)
    published_on = models.DateTimeField()
    content = models.TextField(blank=True)
    content_processed = models.TextField(blank=True)
    author = models.ForeignKey(User)
    published = models.BooleanField(default=False)
    
    class Meta:
        abstract = True

    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return self.content[:128]

    def save(self, *args, **kwargs):
        # For some reason, Django sets the initial value of a TextField to ''
        # instead of None. This means the NOT NULL constraint is never
        # triggered. Setting it to None here does what I want.
        if self.title == '':
            self.title = None

        if self.slug == '':
            self.slug = None

        if self.title and not self.slug:
            self.slug = self.unique_slug_from_title()
        
        self.content_processed = self.content

        return super(Page, self).save(*args, **kwargs)

    def unique_slug_from_title(self):
        slug = slugify(self.title)

        def _check_duplicates(s):
            return self.__class__.objects.filter(
                published_on=self.published_on,
                slug=s
            )

        duplicates = _check_duplicates(slug)
        slug_postfix = 0

        while duplicates:
            slug_postfix += 1
            slug_postfix_str  = '-' + str(slug_postfix)

            # If current slug is too long, truncate it to make room for the
            # postfix.
            if len(slug) >= SLUG_MAXLEN:
                newlen = SLUG_MAXLEN - len(slug_postfix_str)
                slug = slug[:newlen]

            # If the slug ends with a '-', remove it.
            if slug[-1] == '-':
                slug = slug[0:-1]

            slug += slug_postfix_str
            duplicates = _check_duplicates(slug)

        return slug

    @models.permalink
    def get_absolute_url(self):
        current_tz = pytz.timezone(settings.TIME_ZONE)
        published_on_as_current_tz = self.published_on.astimezone(current_tz)
        
        url_args = {
            'year':  published_on_as_current_tz.year,
            'month': published_on_as_current_tz.strftime('%b'),
            'day'  : published_on_as_current_tz.day,
            'slug': self.slug
        }

        return ('cob_journal_entry_detail_view', (), url_args)