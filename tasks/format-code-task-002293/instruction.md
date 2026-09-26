<!--
  If this issue affects many people in a company/big team, create a post for your company in the following discussion:
  https://github.com/pnpm/pnpm/discussions/3787
  and link the issue in your post.

  This will help us prioritize issues that affect more people.
-->

### pnpm version: 7.13.2

### Code to reproduce the issue:

```sh
mkdir -p /var/repo/test
cd /var/repo/test
pnpm init
mkdir lib
# adds { "publishConfig": { "directory": "lib" } } to package.json
cp package.json lib/package.json
pnpm pack --pack-destination /tmp
```

### Expected behavior:
> /tmp/test-1.0.0.tgz

### Actual behavior:
> /var/repo/test/lib/test-1.0.0.tgz

### Additional information:

 - `node -v` prints: v18.10.0
 - Windows, macOS, or Linux?: Linux
