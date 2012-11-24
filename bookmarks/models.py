from django.db import models
from taggit.managers import TaggableManager


class Bookmark(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	title = models.TextField()
	url = models.TextField()
	tags = TaggableManager()

	def __unicode__(self):
		return self.title
