Markdown: should handle punctuation variants
**Prettier 1.8.2-dev ([`ece764a`](https://github.com/prettier/prettier/tree/ece764a0495159af770346842fe704a45e1bb0ee))**

```sh
--parser markdown
```

**Input:**
```markdown
This ia an english paragraph with a CJK quote "中文".

This ia an english paragraph with a CJK quote “中文“.

```

**Output:**
```markdown
This ia an english paragraph with a CJK quote "中文".

This ia an english paragraph with a CJK quote “ 中文 “.

```

**Expected:**
Same as input.

---

![image](https://user-images.githubusercontent.com/8341033/32695926-eac1cdfe-c7a3-11e7-8558-051de09bfc1a.png)

Should use punctuation instead of just ascii punctuation.

https://github.com/prettier/prettier/blob/ece764a0495159af770346842fe704a45e1bb0ee/src/util.js#L14-L17
