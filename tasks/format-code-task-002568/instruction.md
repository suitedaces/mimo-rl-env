## nacl.sealedbox_encrypt / secretbox_* fail to use the configured sk_file / pk_file

I configured nacl on my master with the standard sk_file / pk_file paths
(generated with `salt-call nacl.keygen`) and tried to encrypt a value
without passing the key inline:

```
salt-call --local nacl.sealedbox_encrypt 'hello world'
```

I'd expect this to read the public key from the default `pk_file`
(`/etc/salt/pki/master/nacl.pub`) since I didn't pass `pk=` on the
command line. Instead the call blows up immediately and never produces
a ciphertext. Same thing happens with `nacl.secretbox_encrypt` /
`nacl.secretbox_decrypt` / `nacl.sealedbox_decrypt` when I rely on
`sk_file` rather than passing `sk=` inline.

If I instead pass the key directly, e.g.

```
salt-call --local nacl.sealedbox_encrypt 'hello world' pk='vrwQF7cNi...='
```

it works fine. So the file-based path seems to be the broken one — it
behaves as if `sk_file` / `pk_file` aren't being consulted at all when
no inline key is provided.

Expected: if `sk` / `pk` isn't passed in, fall back to reading from the
configured `sk_file` / `pk_file`. Only complain about "no key" when
neither an inline key nor a readable key file is available.
