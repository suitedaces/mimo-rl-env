MemoryFileSystem duplicates directories
By creating a directory and then creating a file within that directory, `fsspec.implementations.memory.MemoryFileSytem` will register that directory as appearing twice in the original root directory.

## Example

```python
import fsspec
fsspec.__version__
Out[3]: '0.8.2'

from fsspec.implementations.memory import MemoryFileSystem
fs = MemoryFileSystem()
fs.touch('a/b/c.d')
fs.ls('a')
Out[4]: ['a/b/']   # correct

fs = MemoryFileSystem()
fs.mkdir('a/b')
fs.touch('a/b/c.d')
fs.ls('a')
Out[5]: ['a/b/', 'a/b/']   # incorrect
```
