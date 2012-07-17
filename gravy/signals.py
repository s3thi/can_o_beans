from django.core.cache import cache

def clear_cache_on_save(sender, **kwargs):
	cache.clear()