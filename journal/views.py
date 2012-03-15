from django.http import HttpResponse

def show_index(request):
	return show_archive(request)

def show_archive(request, year=None, month=None, day=None):
	return HttpResponse('showing archive')

def show_entry(request, year, month, day, title):
	return HttpResponse('showing a post')
