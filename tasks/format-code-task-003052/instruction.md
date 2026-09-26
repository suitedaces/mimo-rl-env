new:article時にpublication_nameを指定したい
# 概要

記事作成後に都度 publication_name を埋めるのは面倒なので、コマンドオプションで指定できるようにしたいです。

# 実装案

```bash
$ npx zenn  new:article --publication-name myPublication
# => publication_name: "myPublication" を挿入した状態で記事生成
```
