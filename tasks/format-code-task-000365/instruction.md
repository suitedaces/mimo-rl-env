[Bug]: potentially unnecessary parameter is required when submitting OCO orders
### Is there an existing issue for this?

- [X] I have searched the existing issues

### Current Behavior

1) When creating a LImitOrderRequest for an OCO order, an error is returned unless the parameter "limit_price" is also included
2) As a workaround, I use limit_price=1 in all orders. This parameter doesn't seem to be present in the order confirmation details.

### Expected Behavior

1) I assume a LImitOrderRequest is what is needed for an OCO order, since it is used in bracket and OTO orders. 
2) The parameter "limit_price" is not necessary here, because "take_profit" and "stop_loss" are included.

### SDK Version I encountered this issue in

0.14.0

### Steps To Reproduce

```markdown
oco_order_data = LimitOrderRequest(symbol='AAPL', qty=1, side=OrderSide.SELL, time_in_force=TimeInForce.GTC, order_class=OrderClass.OCO, take_profit=TakeProfitRequest(limit_price=300), stop_loss=StopLossRequest(stop_price=50)
```


### Filled out the Steps to Reproduce section?

- [X] I have entered valid steps to reproduce my issue or have attached a minimally reproducible case in code that shows my issue happening; and understand that without this my issue will be flagged as invalid and closed after 30 days.

### Anything else?

Would it be too much to ask for an example of how to submit OCO orders in the sparse documentation?
