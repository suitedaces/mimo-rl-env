When using Dragonfly `IntegerRef` "extras" with the engine language set to German, numbers can't be spoken naturally as whole words. Instead, they must be spoken separately with short pauses. For example, one would have to say "ein und dreissig" instead of "einunddreissig" to match 31.

It should be possible to change Dragonfly's German number implementation ([number.py](https://github.com/dictation-toolbox/dragonfly/blob/master/dragonfly/language/de/number.py)) to accept either way of pronouncing German numbers.

Thanks @tripfish for reporting this on Gitter last month. I should have opened this issue back then, sorry.
