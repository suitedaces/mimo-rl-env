feature: show single-char aliases first in help
If you look at the help message of *nix programs, many of them (especially GNU programs) have a format like this:

<details><summary>Examples (click to expand)</summary>

```console
$ ls --help
  -a, --all                  do not ignore entries starting with .
  -A, --almost-all           do not list implied . and ..
      --author               with -l, print the author of each file
  -b, --escape               print C-style escapes for nongraphic characters
      --block-size=SIZE      scale sizes by SIZE before printing them; e.g.,
                               '--block-size=M' prints sizes in units of
                               1,048,576 bytes; see SIZE format below
  -B, --ignore-backups       do not list implied entries ending with ~
  -c                         with -lt: sort by, and show, ctime (time of last
                               modification of file status information);
                               with -l: show ctime and sort by name;
                               otherwise: sort by ctime, newest first
  -C                         list entries by columns
      --color[=WHEN]         colorize the output; WHEN can be 'never', 'auto',
                               or 'always' (the default); more info below
  -d, --directory            list directories themselves, not their contents
  -D, --dired                generate output designed for Emacs' dired mode
  -f                         do not sort, enable -aU, disable -ls --color
  -F, --classify             append indicator (one of */=>@|) to entries
      --file-type            likewise, except do not append '*'
      --format=WORD          across -x, commas -m, horizontal -x, long -l,
                               single-column -1, verbose -l, vertical -C
      --full-time            like -l --time-style=full-iso
  -g                         like -l, but do not list owner
      --group-directories-first
                             group directories before files;
                               can be augmented with a --sort option, but any
                               use of --sort=none (-U) disables grouping
  -G, --no-group             in a long listing, don't print group names
  -h, --human-readable       with -l, print sizes in human readable format
                               (e.g., 1K 234M 2G)
      --si                   likewise, but use powers of 1000 not 1024
  -H, --dereference-command-line
                             follow symbolic links listed on the command line
      --dereference-command-line-symlink-to-dir
                             follow each command line symbolic link
                               that points to a directory
      --hide=PATTERN         do not list implied entries matching shell PATTERN
                               (overridden by -a or -A)
      --indicator-style=WORD  append indicator with style WORD to entry names:
                               none (default), slash (-p),
                               file-type (--file-type), classify (-F)
  -i, --inode                print the index number of each file
  -I, --ignore=PATTERN       do not list implied entries matching shell PATTERN
  -k, --kibibytes            default to 1024-byte blocks for disk usage
  -l                         use a long listing format
  -L, --dereference          when showing file information for a symbolic
                               link, show information for the file the link
                               references rather than for the link itself
  -m                         fill width with a comma separated list of entries
  -n, --numeric-uid-gid      like -l, but list numeric user and group IDs
  -N, --literal              print raw entry names (don't treat e.g. control
                               characters specially)
  -o                         like -l, but do not list group information
  -p, --indicator-style=slash
                             append / indicator to directories
  -q, --hide-control-chars   print ? instead of nongraphic characters
      --show-control-chars   show nongraphic characters as-is (the default,
                               unless program is 'ls' and output is a terminal)
  -Q, --quote-name           enclose entry names in double quotes
      --quoting-style=WORD   use quoting style WORD for entry names:
                               literal, locale, shell, shell-always, c, escape
  -r, --reverse              reverse order while sorting
  -R, --recursive            list subdirectories recursively
  -s, --size                 print the allocated size of each file, in blocks
  -S                         sort by file size
      --sort=WORD            sort by WORD instead of name: none (-U), size (-S),
                               time (-t), version (-v), extension (-X)
      --time=WORD            with -l, show time as WORD instead of default
                               modification time: atime or access or use (-u)
                               ctime or status (-c); also use specified time
                               as sort key if --sort=time
      --time-style=STYLE     with -l, show times using style STYLE:
                               full-iso, long-iso, iso, locale, or +FORMAT;
                               FORMAT is interpreted like in 'date'; if FORMAT
                               is FORMAT1<newline>FORMAT2, then FORMAT1 applies
                               to non-recent files and FORMAT2 to recent files;
                               if STYLE is prefixed with 'posix-', STYLE
                               takes effect only outside the POSIX locale
  -t                         sort by modification time, newest first
  -T, --tabsize=COLS         assume tab stops at each COLS instead of 8
  -u                         with -lt: sort by, and show, access time;
                               with -l: show access time and sort by name;
                               otherwise: sort by access time
  -U                         do not sort; list entries in directory order
  -v                         natural sort of (version) numbers within text
  -w, --width=COLS           assume screen width instead of current value
  -x                         list entries by lines instead of by columns
  -X                         sort alphabetically by entry extension
  -1                         list one file per line

$ gpg --help
Commands:
 
 -s, --sign                 make a signature
     --clearsign            make a clear text signature
 -b, --detach-sign          make a detached signature
 -e, --encrypt              encrypt data
 -c, --symmetric            encryption only with symmetric cipher
 -d, --decrypt              decrypt data (default)
     --verify               verify a signature
 -k, --list-keys            list keys
     --list-sigs            list keys and signatures
     --check-sigs           list and check key signatures
     --fingerprint          list keys and fingerprints
 -K, --list-secret-keys     list secret keys
     --gen-key              generate a new key pair
     --gen-revoke           generate a revocation certificate
     --delete-keys          remove keys from the public keyring
     --delete-secret-keys   remove keys from the secret keyring
     --sign-key             sign a key
     --lsign-key            sign a key locally
     --edit-key             sign or edit a key
     --passwd               change a passphrase
     --export               export keys
     --send-keys            export keys to a key server
     --recv-keys            import keys from a key server
     --search-keys          search for keys on a key server
     --refresh-keys         update all keys from a keyserver
     --import               import/merge keys
     --card-status          print the card status
     --card-edit            change data on a card
     --change-pin           change a card's PIN
     --update-trustdb       update the trust database
     --print-md             print message digests
     --server               run in server mode

Options:
 
 -a, --armor                create ascii armored output
 -r, --recipient USER-ID    encrypt for USER-ID
 -u, --local-user USER-ID   use USER-ID to sign or decrypt
 -z N                       set compress level to N (0 disables)
     --textmode             use canonical text mode
 -o, --output FILE          write output to FILE
 -v, --verbose              verbose
 -n, --dry-run              do not make any changes
 -i, --interactive          prompt before overwriting
     --openpgp              use strict OpenPGP behavior
```
</details>

Note that single-char aliases are always put first, and any option without a single-char alias is indented to match the `--` of those with a single-char alias.

yargs has this:
```
Options:
  --help, -h     Show help                                             [boolean]
  --version      Show version number                                   [boolean]
  --output, -O   Write output to <file> instead of stdout               [string]
  --quiet, -q    Suppress all normal output                            [boolean]
  --verbose, -v  Explain what is being done                            [boolean]
```
which is not bad but I think putting the single-char aliases first is better:
```
Options:
  -h, --help     Show help                                             [boolean]
      --version  Show version number                                   [boolean]
  -O, --output   Write output to <file> instead of stdout               [string]
  -q, --quiet    Suppress all normal output                            [boolean]
  -v, --verbose  Explain what is being done                            [boolean]
```
