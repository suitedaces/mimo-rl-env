sourmash signature fails in 3.1.0, but sourmash sig works
`sourmash signature merge` fails but `sourmash sig merge` works!

```
(tmp_sgc) tereiter@bm1:~/github/ibd/sandbox/all_sgc_sigs$ sourmash signature merge
sourmash: error: argument cmd: invalid choice: 'signature' (choose from 'categorize', 'compare', 'compute', 'dump', 'gather', 'import_csv', 'index', 'info', 'migrate', 'multigather', 'plot', 'sbt_combine', 'search', 'watch', 'lca', 'sig', 'storage')
```
```
(tmp_sgc) tereiter@bm1:~/github/ibd/sandbox/all_sgc_sigs$ sourmash sig merge
usage:  merge [-h] [-q] [-o FILE] [--flatten] [-k K] [--protein]
              [--no-protein] [--dayhoff] [--no-dayhoff] [--hp] [--no-hp]
              [--dna] [--no-dna]
              signatures [signatures ...]
 merge: error: the following arguments are required: signatures
```
