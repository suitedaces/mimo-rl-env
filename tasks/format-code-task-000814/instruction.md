[BUG] [Formatter] Weired blank lines added when preserve_blank_lines is active
First of all, thanks for this nice tool!

## System Info
 - OS: ubuntu 20.04 (vagrant virtual box provider)
 - Python Version  3.8.10
 - djLint Version  1.7.2
 - template language: django

## Issue
A blank line is inserted in the beginning of the file before most HTML or template tags, when preserve_blank_lines is active.
Also, I noticed some strange new empty lines between multiple \<br />  tags that are separated by spaces.


## How To Reproduce
pyproject.toml:
```
[tool.djlint]
preserve_blank_lines = true
profile = "django"
```
Django template file:

```
{% block someblock %}{% endblock %}
<br/> <br/>
```

Is now reformatted to
```

{% block someblock %}{% endblock %}
<br/>
 
<br/>

```

Note the space in the "empy" line between the \<br/> tags.

I saw, that `extends` is not affected, whereas nearly every other template tag is affected, when placed in the beginning of the file.
I also experienced it with multiple HTML tags when they are placed in the beginning of the file.
