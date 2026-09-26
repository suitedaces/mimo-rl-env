Database url.scheme only works for built-in schemes (backends)
I haven't find any issue related to this topic, so sorry in advance if it is something that has been already discussed.

According to this code inside ```Env.db_url_config()```:
``` python
class Env(object):
    # [...]
   @classmethod
    def db_url_config(cls, url, engine=None):
        # [...]
        if engine:
            config['ENGINE'] = engine
        if url.scheme in Env.DB_SCHEMES:
            config['ENGINE'] = Env.DB_SCHEMES[url.scheme]


        if not config.get('ENGINE', False):
            warnings.warn("Engine not recognized from url: {0}".format(config))
            return {}
```

Actually, the only way to set up a custom backend for a database is using the ```engine``` parameter when we call ```Env.db()``` at the same time that we put an invalid ```url.scheme``` in ```DATABASE_URL``` (what is weird) or we put our custom one again (that it is going to be considered invalid anyway because it doesn't exist in ```Env.DB_SCHEMES```), what is redundant.

``` python
import environ
env = environ.Env()
env.db('DATABASE_URL', engine='path.to.my.custom.backend')
# Having DATABASE_URL=path.to.my.custom.backend://user:password@host:post/database
```

This code fix this situation, simply letting pass the custom scheme as a valid one if it doesn't match one of the built-in ```DB_SCHEMES```.

``` python
if url.scheme in Env.DB_SCHEMES:
    config['ENGINE'] = Env.DB_SCHEMES[url.scheme]
else:
    config['ENGINE'] = url.scheme
```
