## `pass import 1password4pif` loses the username and password fields

I exported my 1Password vault to the `.1pif` format to migrate everything into pass, and ran:

```
pass import 1password4pif my-export.1pif
```

The command finishes without errors and reports a bunch of entries imported. But when I actually look at the imported entries in the store, they're missing the most important parts — the **username** and **password** fields are gone. Other things like the title, URL, and notes seem to make it through fine, but each entry just has the metadata; the actual credentials are not there (or for some entries I see a weird empty-keyed line that looks like two fields collided).

This obviously makes the import useless for me — I have hundreds of logins and I'd have to retype every username and password by hand.

I tried with a fresh export from a current 1Password version, and the `.1pif` file itself does contain my usernames and passwords (I checked by opening it in a text editor — they're in the `secureContents` block of each item, just like the other fields), so the data is there in the input file, it's just not making it into the store on import.

Could the `1password4pif` importer be fixed so that username and password fields are imported along with the rest of the entry?
