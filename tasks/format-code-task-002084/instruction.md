Use a different method for allowing non-TLS redirect URIs
I think requiring an environment variable named `DEBUG` to allow non-TLS redirect URIs isn't the best method. At the very least, it should be named something that won't collide with other libraries (i.e. something like `OAUTHLIB_INSECURE_REDIRECTS`. The best option is to have it be a parameter that is passed instead of a environment variable.

I'd like to incorporate `requests-oauthlib` into a client library for a web API. Having users of my library set a `DEBUG` environment variable isn't something I want to force on users.

I'm happy to post a patch, but I'd like to get feedback first.
