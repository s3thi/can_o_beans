from django.conf.urls.defaults import patterns, include, url

y = '(?P<year>\d{4})'
m = '(?P<month>\w+)'
d = '(?P<day>\d{2})'
t = '(?P<title>\w+)'

urlpatterns = patterns('journal.views',
	url('^{0}/$'.format(y), 'show_archive'),
	url('^{0}/{1}/$'.format(y, m), 'show_archive'),
	url('^{0}/{1}/{2}/$'.format(y, m, d), 'show_archive'),
	url('^{0}/{1}/{2}/{3}/$'.format(y, m, d, t), 'show_post'),
)
