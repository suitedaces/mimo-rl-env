Handle hash capitalization
Windows users will likely hit an issue when making a data manifest file as most guidance online shows finding the SHA256 of a file in power shell like this:

```
Get-FileHash myfile.bin | Format-List
```

Which then produces output like

```
Algorithm : SHA256
Hash      : 7268E3A01D57CCE828BCB7E0FF82F9048AB3A70520C58516A1145B51F7032A1D
Path      : C:\Users\myuser\myfile.bin
```

If that hash is pasted right into the manifest file pooch will try to update the file as the caps in the hash don't match strictly. I don't *believe* there would be any follow on consequences of running info read from the manifest through `.lower()` before checking for a hash match?
