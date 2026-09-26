convert_pkg_info raises an exception if the description is empty
`description_lines[0].lstrip()` raises a `list index out of range` exception if the description field is empty. Here's a minimal repro:

`Parser().parsestr('description:\n')['description'].splitlines()[0]`

The fix is to check if the description is empty before calling splitlines on it
