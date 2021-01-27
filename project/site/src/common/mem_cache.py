from django.core.cache.backends.locmem import LocMemCache


class MemCache(LocMemCache):
    def validate_key(self, *args, **kwargs):
        pass
