from django.conf.urls.defaults import patterns, url
from bookmarks import views


urlpatterns = patterns('',
	url(r'^$', views.ListBookmarksView.as_view(), name='bookmarks_list'),	
	url(r'^tagged/(?P<tags>[a-zA-Z0-9+-_]+)/$',
		views.TaggedBookmarksView.as_view(), name='bookmarks_tagged'),
	url(r'^hostname/(?P<hostname>.+)/$', views.HostnameBookmarksView.as_view(),
		name='bookmarks_hostname'),
	
	url(r'^new/$', views.CreateBookmarkView.as_view(), name='bookmark_create'),
	url(r'^edit/(?P<id>\d+)/$', views.EditBookmarkView.as_view(), name='bookmark_edit'),
)
