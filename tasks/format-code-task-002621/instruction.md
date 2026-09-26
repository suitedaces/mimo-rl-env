## `SOMEIP.fragment()` returns empty fragments when the payload lives in `data`

I'm working with `scapy.contrib.automotive.someip.SOMEIP` to handle a custom SOME/IP service. The `SOMEIP` class exposes `data` as a `PacketListField` and dispatches per-service payload classes through `SOMEIP.payload_cls_by_srv_id` / `get_payload_cls_by_srv_id`, so I register my own payload class for the service id I care about:

```python
from scapy.contrib.automotive.someip import SOMEIP

class MyPayload(Packet):
    name = "MyPayload"
    fields_desc = [StrField("blob", b"")]

SOMEIP.payload_cls_by_srv_id[0x1234] = MyPayload
```

After this, when I build (or receive and parse) a SOMEIP packet for service `0x1234`, my payload ends up in `pkt.data[0]`, which is what I'd expect from how this dispatch is set up.

Now I want to send this through SOME/IP-TP, so I switch the message type to a TP one and call `fragment()`:

```python
pkt = SOMEIP(
    srv_id=0x1234,
    msg_type=SOMEIP.TYPE_TP_REQUEST,
    data=[MyPayload(blob=b"\x00" * 5000)],
)

fragments = pkt.fragment(fragsize=512)

for f in fragments:
    print(len(raw(f)), raw(f)[-32:])
```

The fragments I get back don't contain any of the bytes from `MyPayload.blob`. Each one looks the size of an empty SOMEIP-TP header — it's as if `fragment()` doesn't see my payload at all and just produces a bunch of empty TP segments with `more_seg` toggled.

I'd expect `fragment(fragsize=N)` to slice the actual payload bytes into chunks of size `N` and emit one SOMEIP-TP packet per chunk carrying that slice, regardless of how the payload is attached to the SOMEIP packet — given that storing the payload inside `data` is the path the class itself documents through `payload_cls_by_srv_id`.
