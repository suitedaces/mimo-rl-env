make `localforage.config` fail if `version` is not a number
I set my `version` to a string value because I saw `1.0` in the [documentation](http://mozilla.github.io/localForage/#config) and just about every system I use that uses the dotted notation for version numbers treats version numbers as strings (because they typically support `major.minor.patch`). I did not notice the lack of quotes around it.

My fault, but it would be helpful to have `localforage.config` fail if the version number is a string. Why? IndexedDB in FF and Chrome will be happy with `"1.0"`, but IE's IndexedDB will throw `InvalidAccessError`.

Moreover, one of localForage's features is the ability to switch to a different driver if desired. I take it from reading the webSQL standard that it takes a string as a version number when opening a database. Someone who had code working fine with a version number set to a string value (e.g. "1.3a") because they used the webSQL or localStorage drivers will find their code failing if it runs with the IndexedDB driver.
