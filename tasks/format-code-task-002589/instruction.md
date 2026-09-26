# Problem Statement

I’m trying to use `num2words` for Kazakh text, but `lang='kz'` isn’t supported right now. Could you add Kazakh number spelling, including negatives/decimals and common currency amounts like KZT and USD?

# Expected outcomes

- Kazakh cardinal numbers: `num2words(number, lang='kz')` should be supported for zero, single digits, tens, hundreds, and larger grouped values such as thousands, millions, and billions, returning standard Kazakh number words instead of raising an unsupported-language error.
- Negative Kazakh numbers: `num2words(negative_number, lang='kz')` should return Kazakh text prefixed with `минус`.
- Decimal Kazakh numbers: `num2words(decimal_number, lang='kz')` should spell the integer and fractional parts in Kazakh, joined with `бүтін`.
- Currency amounts: `num2words(amount, lang='kz', to='currency', currency='KZT')` should spell tenge amounts using `теңге` and `тиын`; `num2words(amount, lang='kz', to='currency', currency='USD')` should spell dollar amounts using `доллар` and `цент`.
- Documentation: the supported-language list in `README.rst` should include Kazakh with the language code `kz`.

# Implementation notes

- Match the existing public `num2words` API conventions for adding language support; the concrete module structure, helper functions, and internal data representation are up to the implementer.
- Keep behavior observable through the existing API and documentation surfaces; no particular internal class, constant, or helper name is required.
- Implement only behavior needed for Kazakh cardinal, negative, decimal, and KZT/USD currency spelling unless the existing project conventions require additional stubs or defaults.
