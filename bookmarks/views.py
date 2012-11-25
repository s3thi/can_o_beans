from functools import wraps
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.views import login
from bookmarks.models import Bookmark
from bookmarks.forms import BookmarkForm


BOOKMARKS_PER_PAGE = 50


def staff_member_required(view_func):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, displaying the login page if necessary. This is stolen straight
    from the Django source code.
    """
    @wraps(view_func)
    def _checklogin(request, *args, **kwargs):
        if request.user.is_active and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        return login(request, extra_context={'next': request.get_full_path()})

    return _checklogin


class StaffMemberRequiredMixin(object):
    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(StaffMemberRequiredMixin, self).dispatch(*args, **kwargs)


class ListBookmarksView(ListView):
	template_name = 'bookmarks/bookmarks_list.html'
	paginate_by = BOOKMARKS_PER_PAGE

	def get_queryset(self):
		if self.request.user.is_authenticated():
			return Bookmark.objects.order_by('-created')
		else:
			return Bookmark.objects.filter(private=False).order_by('-created')


class TaggedBookmarksView(ListView):
	template_name = 'bookmarks/bookmarks_tagged.html'
	paginate_by = BOOKMARKS_PER_PAGE

	def _get_tags(self):
		return self.kwargs['tags'].split('+')

	def get_queryset(self):
		# This is very inefficient, but it won't be an issue during actual
		# operation since the number of tags is likely to be very small (mostly
		# just one).
		
		tags = self._get_tags()
		qs = Bookmark.objects.all()
		
		for tag in tags:
			qs = qs.filter(tags__name__in=[tag,])
		
		return qs

	def get_context_data(self, *args, **kwargs):
		context = super(TaggedBookmarksView, self).get_context_data(
			*args, **kwargs
		)

		context['tags'] = self._get_tags()
		return context


class HostnameBookmarksView(ListView):
	template_name = 'bookmarks/bookmarks_hostname.html'
	paginate_by = BOOKMARKS_PER_PAGE

	def get_queryset(self):
		return Bookmark.objects.filter(hostname=self.kwargs['hostname'])

	def get_context_data(self, *args, **kwargs):
		context = super(HostnameBookmarksView, self).get_context_data(
			*args, **kwargs
		)

		context['hostname'] = self.kwargs['hostname']
		return context


class CreateBookmarkView(StaffMemberRequiredMixin, CreateView):
	model = Bookmark
	template_name = 'bookmarks/bookmark_create.html'
	form_class = BookmarkForm
	success_url = reverse_lazy('bookmarks_list')

	def get_initial(self, *args, **kwargs):
		initial = super(CreateBookmarkView, self).get_initial(*args, **kwargs)
		
		initial['title'] = self.request.GET.get('title', '')
		initial['url'] = self.request.GET.get('url', '')
		
		return initial
