## Support for Django's built-in Redis cache backend

I'm on Django 4.2 and using the Redis cache backend that ships with Django itself (`django.core.cache.backends.redis.RedisCache`, available since Django 4.0). I'd like to track cache hits/misses with django-prometheus.

Looking at the docs and `django_prometheus.cache.backends`, the only Redis option provided is a wrapper around the third-party `django-redis` package. So in order to get the hit/miss/error metrics for my Redis cache, it looks like I'd have to add `django-redis` to my project just to satisfy django-prometheus, even though Django already ships a perfectly good Redis backend out of the box.

My `CACHES` setting today looks roughly like this:

```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
    }
}
```

I'd like to be able to point `BACKEND` at something from `django_prometheus` and start seeing the same kind of metrics that the existing `django-redis` wrapper exposes (hits, misses, total gets, failed gets), but without pulling in `django-redis` as an additional dependency. As far as I can tell there is currently no such wrapper for the stdlib Redis backend.

Would it be possible to add first-class support for Django's built-in Redis cache backend in `django_prometheus.cache.backends.redis`, alongside the existing `django-redis`-based one? The new wrapper class would be something like `NativeRedisCache`, and its metrics should be distinguishable from the existing `django-redis` ones via a separate backend label (e.g. `native_redis`).
