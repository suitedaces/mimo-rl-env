## Test accounts can't sign EIP712 messages

I'm writing tests for a contract that uses EIP712 signatures (it's an ERC-2612 `permit`-style flow, so I need to construct a typed `Permit` message and have an account sign it). For the live network the signing works through my real account, but in the ape test suite I want to use one of the built-in test accounts so the test is hermetic.

Roughly what I'm doing:

```python
from eip712.messages import EIP712Message

class Permit(EIP712Message):
    _name_ = "MyToken"
    _version_ = "1"
    _chainId_ = 1
    _verifyingContract_ = token.address

    owner: "address"
    spender: "address"
    value: "uint256"
    nonce: "uint256"
    deadline: "uint256"

def test_permit(accounts, token):
    owner = accounts[0]   # an ape_test TestAccount
    spender = accounts[1]

    msg = Permit(
        owner=owner.address,
        spender=spender.address,
        value=1000,
        nonce=0,
        deadline=2**32,
    )

    sig = owner.sign_message(msg)
    assert sig is not None       # <- fails
    token.permit(owner, spender, 1000, 2**32, sig.v, sig.r, sig.s, sender=spender)
```

`owner.sign_message(msg)` just gives me back `None`, so the assertion blows up and I can never get to the `permit` call. Plain string messages signed against the same test account work fine, it's specifically the EIP712 typed message that comes back empty.

It'd be great if the `ape_test` accounts could sign EIP712 messages the same way they handle the other message types, so tests that exercise `permit` / EIP712-based auth flows can actually run end-to-end without a real key.
