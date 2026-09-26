## Common shell commands aren't highlighted as built-ins in `bash`

I'm using highlight.js on my docs site to render shell snippets, and the most-used commands look completely unstyled while rare shell internals show up colored. Take a typical snippet:

```bash
mkdir -p /tmp/build
cp src/* /tmp/build/
ls -la /tmp/build
chmod +x /tmp/build/run.sh
mv /tmp/build/output.log /var/log/
cat /var/log/syslog | head -n 50 | sort | wc -l
echo "done"
```

When this is rendered as `language-bash`, `echo` (and things like `printf`, `pwd`, `set`) get the built-in styling, but `mkdir`, `cp`, `ls`, `chmod`, `mv`, `cat`, `head`, `sort`, `wc` are all rendered as plain text — same color as filenames and arguments. The visual outcome is that the everyday GNU core utilities — which is basically what people actually write in shell scripts 99% of the time — look unrecognized, while the obscure shell-internal stuff stands out. Side-by-side it looks really inconsistent.

It would be great if the standard GNU core utilities were treated as built-ins by the bash grammar too, so a normal shell snippet looks uniformly highlighted.
