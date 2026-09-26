## Wrong order / negative duration when parsing cross-year date ranges like "from November 15 to January 5"

I'm using the date-time recognizer to parse free-form date ranges. When the user writes a range without explicit years and the range happens to cross a year boundary, the parsed result comes back inconsistent.

### Repro

JavaScript (`@microsoft/recognizers-text-date-time`), reference date around early December 2018 (the exact day doesn't matter much, anything in late autumn / early winter reproduces it):

```js
const recognizer = new DateTimeRecognizer(Culture.English);
const model = recognizer.getDateTimeModel();
const result = model.parse("from November 15 to January 5", new Date(2018, 11, 1));
console.log(JSON.stringify(result, null, 2));
```

The same thing happens in Python with `recognizers_date_time`.

### What I get

The resolution for the `daterange` entity looks broken:

- The `timex` ends up looking like `(XXXX-11-15,XXXX-01-05,P-314D)` — note the **negative** `P-314D`. The duration of a date range should never be negative.
- The `futureValue` array has the begin date *after* the end date (next-year November vs. next-year January), so iterating `[begin, end]` as a real interval is meaningless.
- The `pastValue` side has a symmetric problem in some cases too — the past end can land before the past begin.

### What I expected

For an input like "from November 15 to January 5" parsed near year end, I expect the future projection to roll forward sensibly — e.g. begin = November 15 of the current year, end = January 5 of the next year — so that `begin <= end` and the day count in the timex is a non-negative number. Whichever exact years the parser picks, the begin/end of any one resolution (future or past) should be in chronological order.

Right now it's effectively unusable for any range expression that crosses Dec 31 without explicit years, because downstream code that does `(end - begin)` on the resolution gets garbage.
