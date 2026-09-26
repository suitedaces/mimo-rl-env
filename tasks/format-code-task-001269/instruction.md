Add or enable a strict version of 'activate' decorator
Decorator `activate` is easier to use in some cases, but sadly it never checks, if all requests were used. Similar decorator with `assert_all_requests_are_fired=True`, or a possibility to turn it on, would be helpful.
