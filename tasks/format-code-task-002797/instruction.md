v2 to v3 theme() keys bug?
**What version of Tailwind CSS are you using?**

v3.0.1

**What build tool (or framework if it abstracts the build tool) are you using?**

vue cli v5.x webpack v5.x

**What version of Node.js are you using?**

v16.5.0

**What browser are you using?**

N/A

**What operating system are you using?**

macOS

**Describe your issue**

Develop or compile. This message always appears

```
 does not exist in your theme config. 'spacing' has the following keys: '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '14', '16', '18', '20', '24', '28', '32', '36', '40', '44', '48', '52', '56', '60', '64', '72', '80', '96', 'px', '0.5', '1.5', '2.5', '3.5', '4.5', '7.5'

  17 | }
  18 | .dialog.iOS .title {
> 19 |   font-size: theme("spacing['4.5']");
     |   ^
  20 |   color: theme("colors.black");
  21 | }
```

But the following keys message contains the index

There is no such error message in v2

tailwind.config.js

```
module.exports = {
  theme: {
    spacing: {
      ["4.5"]: "1.125rem"
    },
  }
}
```
