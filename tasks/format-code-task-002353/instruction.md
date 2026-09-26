Please offer a way to exclude dirs *in addition to the default exclusions*
**Is your feature request related to a problem? Please describe.**

I needed to exclude one auto-generated file so I naively specified `--exclude thefile.py`. Unfortunately that disabled the useful standard exclusions, which I did not realize until it broke a unit test running on Jenkins.

**Describe the solution you'd like**

I would like a way to exclude one or more files or directories *in addition to the standard exclusion defaults*.

**Describe alternatives you've considered**

The simplest UI change would be a new command-line option such as `--alsoexclude` meaning "exclude the specified files and directories in addition to other exclusions." The example above would read `--alsoexclude thefile.py`.

Please also consider allowing that option to be repeated. It seems a very natural thing and it saves the hassle of generating a regex to exclude multiple items. Thus: `--alsoexclude foo.py --alsoexclude .private --alsoexclude a/path/somewhere`. 

Ideally I would suggest that same capability for `--exclude` and `--include`, because regular expressions can be hard to read and can easily have subtle bugs. But I realize that is a stretch since it changes an existing interface.

Another option is to add a boolean option that means "exclude the standard defaults", such as `--excludedefaults`. Then the example above would read `--excludedefaults --exclude thefile.py`

Yet another option is to have some magic value that means "the standard exclusion defaults". But I don't know what it could be without risking collision with files and directory names.

**Additional context**

None.
