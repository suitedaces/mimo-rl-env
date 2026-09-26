## Refactor: `_ccxt_config` is duplicated across exchange subclasses

While working on the leverage / trading-mode code I noticed that several exchange subclasses (`Binance`, `Gateio`, `Okex`, …) all override `_ccxt_config` with essentially the same body:

```python
@property
def _ccxt_config(self) -> Dict:
    if self.trading_mode == TradingMode.MARGIN:
        return {"options": {"defaultType": "margin"}}
    elif self.trading_mode == TradingMode.FUTURES:
        return {"options": {"defaultType": "<something>"}}
    else:
        return {}
```

The only thing that actually differs between exchanges is the `defaultType` string used for futures — Binance wants one value, Gate.io / OKEx want another, Bybit wants yet another. Everything else (the margin branch, the spot fallback, the shape of the dict) is copy-pasted. Adding a new futures-capable exchange today means duplicating this block again, and any change to the structure has to be done in N places.

It would be much cleaner if the base `Exchange` class handled the generic margin / futures / spot logic itself, and each subclass only declared its exchange-specific futures market type in the place where they already declare other per-exchange quirks. New futures exchanges would then get the right ccxt config "for free" as long as they declare what kind of futures market they use, without re-implementing the same property.

There's also a related wrinkle: `Bibox` overrides `_ccxt_config` to return `{"has": {"fetchCurrencies": False}}`. Once the base class actually returns something non-empty, that override would silently drop whatever the base class wants to contribute (e.g. the margin/futures options), so subclasses that need to add their own keys should still end up with the base config merged in rather than replaced.

Could we consolidate `_ccxt_config` into the base `Exchange` and have subclasses contribute only the exchange-specific bits? For reference on the futures market type values: Bybit's ccxt futures market is `"linear"` (the other exchanges without an explicit override should fall back to the common default).
