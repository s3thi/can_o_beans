from django.db import models
from django.contrib.auth.models import User

class JournalEntry(models.Model):
	title = models.CharField(max_length=512, blank=True, null=True)
	published_on = models.DateTimeField()
	content = models.TextField()
	author = models.ForeignKey(User)

	def __unicode__(self):
		if self.title:
			return '<{0}>'.format(self.title)
		else:
			humanized_date = self.published_on.strftime('%b %d, %Y')
			return '<{0}: {1}>'.format(humanized_date, self.content[:128])
