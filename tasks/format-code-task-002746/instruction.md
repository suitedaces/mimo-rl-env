Network passphrase is easy to accidentally get wrong
**Describe the bug**
The [runtime warning](https://github.com/stellar/js-stellar-base/blob/64785eb2e3dfece3b28e3c3767edaa6b8e09bb06/src/transaction.js#L31-L35) when passing a bad `networkPassphrase` to a `new Transaction` is easy to miss. The [laboratory had incorrect behavior](https://github.com/stellar/laboratory/pull/429/files) for a number of weeks and a stronger warning might have caught it earlier. 

**What version are you on?**
2.1.2

**To Reproduce**
1. Pass something other than a string to `new Transaction(envelope, garbagePassphrase)`.
2. See deprecation warning in console at runtime.

**Expected behavior**
A strong signal that an incorrect argument was passed.

**Additional context**
Add any other context about the problem here.
