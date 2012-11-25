from django.db import models
from urlparse import urlparse
from taggit.managers import TaggableManager


class Bookmark(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	title = models.TextField()
	url = models.URLField()
	hostname = models.TextField(blank=True)
	tags = TaggableManager(blank=True)
	note = models.TextField(blank=True)
	private = models.BooleanField(default=False)

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.hostname = urlparse(self.url).hostname
		super(Bookmark, self).save(*args, **kwargs)
