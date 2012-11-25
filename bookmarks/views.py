from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from bookmarks.models import Bookmark
from bookmarks.forms import BookmarkForm


class ListBookmarksView(ListView):
	queryset = Bookmark.objects.order_by('-created')
	template_name = 'bookmarks/bookmarks_list.html'


class TaggedBookmarksView(ListView):
	pass


class HostnameBookmarksView(ListView):
	pass


class CreateBookmarkView(CreateView):
	model = Bookmark
	template_name = 'bookmarks/bookmark_create.html'
	form_class = BookmarkForm
	success_url = reverse_lazy('bookmarks_list')

	def get_initial(self, *args, **kwargs):
		initial = super(CreateBookmarkView, self).get_initial(*args, **kwargs)
		
		initial['title'] = self.request.GET.get('title', '')
		initial['url'] = self.request.GET.get('url', '')
		
		return initial
