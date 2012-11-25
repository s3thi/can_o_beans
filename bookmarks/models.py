from django.db import models
from urlparse import urlparse
from taggit.managers import TaggableManager


class Bookmark(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	title = models.TextField()
	url = models.URLField()
	tags = TaggableManager(blank=True)
	note = models.TextField(blank=True)
	private = models.BooleanField(default=False)

	def __unicode__(self):
		return self.title

	def hostname(self):
		return urlparse(self.url).hostname 
