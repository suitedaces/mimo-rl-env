False positive 434: toggling a boolean
### What's wrong

The following code triggers a WPS434 violation warning.

```python
in_code_block = not in_code_block
```

### How it should be

No warning. There's no better way to toggle a boolean.

### Flake8 version and plugins

```json
{
  "dependencies": [],
  "platform": {
    "python_implementation": "CPython",
    "python_version": "3.8.12",
    "system": "Linux"
  },
  "plugins": [
    {
      "is_local": false,
      "plugin": "black",
      "version": "0.2.3"
    },
    {
      "is_local": false,
      "plugin": "flake8-bandit",
      "version": "2.1.2"
    },
    {
      "is_local": false,
      "plugin": "flake8-bugbear",
      "version": "21.9.1"
    },
    {
      "is_local": false,
      "plugin": "flake8-comprehensions",
      "version": "3.6.1"
    },
    {
      "is_local": false,
      "plugin": "flake8-darglint",
      "version": "1.8.0"
    },
    {
      "is_local": false,
      "plugin": "flake8-docstrings",
      "version": "1.6.0, pydocstyle: 6.1.1"
    },
    {
      "is_local": false,
      "plugin": "flake8-pytest-style",
      "version": "1.5.0"
    },
    {
      "is_local": false,
      "plugin": "flake8-string-format",
      "version": "0.3.0"
    },
    {
      "is_local": false,
      "plugin": "flake8-tidy-imports",
      "version": "4.4.1"
    },
    {
      "is_local": false,
      "plugin": "flake8-variables-names",
      "version": "0.0.4"
    },
    {
      "is_local": false,
      "plugin": "flake8_builtins",
      "version": "1.5.2"
    },
    {
      "is_local": false,
      "plugin": "mccabe",
      "version": "0.6.1"
    },
    {
      "is_local": false,
      "plugin": "naming",
      "version": "0.12.1"
    },
    {
      "is_local": false,
      "plugin": "pycodestyle",
      "version": "2.7.0"
    },
    {
      "is_local": false,
      "plugin": "pyflakes",
      "version": "2.3.1"
    },
    {
      "is_local": false,
      "plugin": "wps-light",
      "version": "0.15.3"
    }
  ],
  "version": "3.9.2"
}
```

### pip information

pip 21.2.4 from /home/pawamoy/.local/lib/python3.8/site-packages/pip (python 3.8)

Not using pip to manage packages.

### OS information

GNU/Linux 5.14.6
