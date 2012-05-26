from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse


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

    title = models.TextField(blank=False, null=False)
    slug = models.SlugField(max_length=SLUG_MAXLEN, blank=True, null=True)
    published_on = models.DateTimeField()
    content = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User)
    
    class Meta:
        abstract = True

    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return self.content[:128]

    def save(self, *args, **kwargs):
        if self.title and not self.slug:
            self.slug = self.unique_slug_from_title()
        # Why do I have to check this here? I already _said_ in the model
        # that I don't want title to be NULL or blank.
        elif not self.title:
           raise IntegrityError('title can\'t be null or blank')

        try:
            int(self.slug)
        except:
            pass
        else:
            # TODO: test this condition.
            raise IntegrityError('slug cannot be an integer')
        
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
            if len(slug) == SLUG_MAXLEN:
                newlen = SLUG_MAXLEN - len(slug_postfix_str)
                slug = slug[:newlen]

            # If the slug ends with a '-', remove it.
            if slug[-1] == '-':
                slug = slug[0:-1]

            slug += slug_postfix_str
            duplicates = check_duplicates(slug)

        return slug

    def url(self):
        args = {
            'year': self.published_on.year,
            'month': self.published_on.strftime('%b'),
            'day'  : self.published_on.day
        }

        if self.slug:
            args['slug'] = self.slug
            return reverse('cob_journal_entry_detail_view', kwargs=args)
        else:
            args['pk'] = self.id
            return reverse('cob_journal_entry_detail_view_pk', kwargs=args)
