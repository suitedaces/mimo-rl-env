Inheritance works with task parameters e.g:

```ini
[runtime]
    [[FAM<param>]]
    [[task<param>]]
        inherit = FAM<param>
```

However, when mixing parameters across inheritance it only partially works.

```ini
[runtime]
    [[FAM<param1>]]
    [[task<param2>]]
        inherit = FAM<param1>
```

### Example

```ini
[task parameters]
    a = 1..2
    b = 1..2

[scheduling]
    [[graph]]
        R1 = """
            <a>
        """

[runtime]
    [[<a>]]
        inherit = <b=1>
        script = test $b -eq 1

    [[<b>]]
        [[[environment]]]
            b = %(b)d
```

The inheritance does indeed work as shown by the output of `cylc config`:

```console
$ cylc config --sparse  param-test 
[task parameters]
    a = 1, 2
    b = 1, 2
[scheduling]
    cycling mode = integer
    initial cycle point = 1
    final cycle point = 1
    [[graph]]
        R1 = <a>
[runtime]
    [[root]]
    [[_a1]]
        inherit = _b1
        script = test $b -eq 1
        [[[environment]]]
            b = %(b)d
    [[_a2]]
        inherit = _b1
        script = test $b -eq 1
        [[[environment]]]
            b = %(b)d
    [[_b1]]
        [[[environment]]]
            b = %(b)d
    [[_b2]]
        [[[environment]]]
            b = %(b)d
[visualization]
    [[node attributes]]
```

However, the parameter in the environment variable is not expanded in the job script:

```bash
# job

cylc__job__inst__user_env() {
    # TASK RUNTIME ENVIRONMENT:
    export b
    b="%(b)d"
}
```

### Use Case

Example use case which involves mapping one parameter onto another:

```ini
[runtime]
    # define environments
    [[environment<environment>]]

    # map models onto environments
    [[model<model=a>]]
        inherit = environment<1>
    [[model<model=b>]]
        inherit = environment<2>
    [[model<model=c>]]
        inherit = environment<1>
```
