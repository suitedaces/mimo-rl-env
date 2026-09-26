I want Funcy to provide pure nested path helpers for dictionaries and lists.

I need get_in(coll, path, default=None) to walk coll[key] for each key in path and return the nested value. For get_in({'a': {'b': 42}}, ['a', 'b']) it should return 42, and for get_in({'x': [1, 2]}, ['x', 1]) it should return 2. Missing keys or list indexes should return the default, so get_in({'a': 1}, ['b'], 'fallback') returns 'fallback'. If an object along the path cannot be indexed with the supplied key type, get_in should raise TypeError, for example get_in([1, 2], ['a']).

I also need get_lax(coll, path, default=None) with the same successful lookup behavior, but it should return the default instead of raising TypeError for incompatible path steps. For example, get_lax([1, 2], ['a'], 'fallback') returns 'fallback', and get_lax({'a': None}, ['a', 'b']) returns None.

I need set_in(coll, path, value) to return a modified copy with the nested value assigned without mutating the original input. For example, set_in({'a': {'b': 1}}, ['a', 'b'], 7) returns {'a': {'b': 7}}, while the original nested value remains 1. It should create missing dictionary branches as needed, so set_in({}, ['a', 'b'], 42) returns {'a': {'b': 42}}, and it should also support list indexes like set_in([{}, 1], [1], 7) returning [{}, 7].

I need update_in(coll, path, update, default=None) to return a modified copy where the value at path is replaced by update(current_value). For example, update_in({'c': []}, ['c'], len) returns {'c': 0}, and update_in({}, ['a', 'b'], lambda x: x + 1, default=0) returns {'a': {'b': 1}}.

I need del_in(coll, path) to return a modified copy with a nested dictionary key or list index removed. For del_in({'c': [1, 2, 3]}, ['c', 1]) it should return {'c': [1, 3]}. An empty path or a missing key/index should leave the original object unchanged, while an incompatible path step such as del_in({'c': [1, 2, 3]}, ['c', 'b']) should raise TypeError.

I need has_path(coll, path) to report whether every step exists. It should return True for has_path({'a': {'b': 42}}, ['a', 'b']) and has_path({'x': [1, 2]}, ['x', 1]), and False for missing keys or indexes such as has_path({'a': {'b': 42}}, ['c']) and has_path([1, 2], [3]). These helpers should be deterministic, should not mutate the input collection, and should not do filesystem, network, or global-state work.
