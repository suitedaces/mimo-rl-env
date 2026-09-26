[Bug]: pydantic ValidationError when calling close_all_positions
### Is there an existing issue for this?

- [X] I have searched the existing issues

### Current Behavior

When I run the code in **Steps To Reproduce** I get the error posted in **Anything else?**.

Not much else to add.

### Expected Behavior

_No response_

### SDK Version I encountered this issue in

0.10

### Steps To Reproduce

```markdown
trading_client = TradingClient(alpaca_key, secret, url_override='https://api.alpaca.markets')
trading_client.close_all_positions(cancel_orders=False)
```


### Filled out the Steps to Reproduce section?

- [X] I have entered valid steps to reproduce my issue or have attached a minimally reproducible case in code that shows my issue happening; and understand that without this my issue will be flagged as invalid and closed after 30 days.

### Anything else?

Traceback (most recent call last):
  File "C:\Users\Ben\PycharmProjects\StockTrader\main.py", line 418, in <module>
    print(trading_client.close_all_positions(cancel_orders=True))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Ben\PycharmProjects\StockTrader\venv\Lib\site-packages\alpaca\trading\client.py", line 287, in close_all_positions
    return parse_obj_as(List[ClosePositionResponse], response)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "pydantic\tools.py", line 38, in pydantic.tools.parse_obj_as
  File "pydantic\main.py", line 341, in pydantic.main.BaseModel.__init__
    account = trading_client.get_account()
pydantic.error_wrappers.ValidationError: 18 validation errors for ParsingModel[List[alpaca.trading.models.ClosePositionResponse]]
__root__ -> 0 -> body -> available
  field required (type=value_error.missing)
__root__ -> 0 -> body -> existing_qty
  field required (type=value_error.missing)
__root__ -> 0 -> body -> held_for_orders
  field required (type=value_error.missing)
__root__ -> 0 -> body -> symbol
  field required (type=value_error.missing)
__root__ -> 0 -> body -> id
  field required (type=value_error.missing)
__root__ -> 0 -> body -> client_order_id
  field required (type=value_error.missing)
__root__ -> 0 -> body -> created_at
  field required (type=value_error.missing)
__root__ -> 0 -> body -> updated_at
  field required (type=value_error.missing)
__root__ -> 0 -> body -> submitted_at
  field required (type=value_error.missing)
__root__ -> 0 -> body -> asset_id
  field required (type=value_error.missing)
__root__ -> 0 -> body -> symbol
  field required (type=value_error.missing)
__root__ -> 0 -> body -> asset_class
  field required (type=value_error.missing)
__root__ -> 0 -> body -> order_type
  field required (type=value_error.missing)
__root__ -> 0 -> body -> type
  field required (type=value_error.missing)
__root__ -> 0 -> body -> side
  field required (type=value_error.missing)
__root__ -> 0 -> body -> time_in_force
  field required (type=value_error.missing)
__root__ -> 0 -> body -> status
  field required (type=value_error.missing)
__root__ -> 0 -> body -> extended_hours
  field required (type=value_error.missing)
