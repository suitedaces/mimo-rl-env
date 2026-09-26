[gatsby-remark-images]: bug: uses filename as alt text when showCaptions is true
## Description

Since https://github.com/gatsbyjs/gatsby/pull/13489, when using `showCaptions:true` `gatsby-remark-images` inserts the file name, when using the standard img snippet:

```
![](./img.jpg)
```

### Steps to reproduce
1. Enable showCaptions:true with latest version of plugin
2. Add `![](./img.jpg)` to a markdown

### Expected result
Shouldn't be any caption shown

### Actual result
The file name is inserted as caption

### Temporary workaround
You can insert a space between [ ], and then a space is shown instead, at least not visible.


### Environment

```

  System:
    OS: macOS 10.14.4
    CPU: (8) x64 Intel(R) Core(TM) i7-4750HQ CPU @ 2.00GHz
    Shell: 3.2.57 - /bin/bash
  Binaries:
    Node: 8.15.1 - ~/n/bin/node
    Yarn: 1.15.2 - /usr/local/bin/yarn
    npm: 6.4.1 - ~/n/bin/npm
  Languages:
    Python: 2.7.16 - /usr/local/bin/python
  Browsers:
    Chrome: 74.0.3729.157
    Firefox: 66.0.5
    Safari: 12.1
  npmPackages:
    gatsby: 2.5.x => 2.5.6 
    gatsby-image: ^2.1.0 => 2.1.0 
    gatsby-plugin-react-helmet: ^3.0.12 => 3.0.12 
    gatsby-plugin-sass: ^2.0.11 => 2.0.11 
    gatsby-plugin-sharp: ^2.0.37 => 2.0.37 
    gatsby-remark-copy-linked-files: ^2.0.12 => 2.0.12 
    gatsby-remark-images: 3.x => 3.0.11 
    gatsby-remark-prismjs: ^3.2.9 => 3.2.9 
    gatsby-remark-responsive-iframe: ^2.1.1 => 2.1.1 
    gatsby-remark-smartypants: ^2.0.9 => 2.0.9 
    gatsby-source-filesystem: ^2.0.36 => 2.0.36 
    gatsby-transformer-remark: ^2.3.12 => 2.3.12 
    gatsby-transformer-sharp: ^2.1.19 => 2.1.19 
  npmGlobalPackages:
    gatsby-cli: 2.5.15
```
