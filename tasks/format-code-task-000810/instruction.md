## `skip_unchanged` skips rows where only the M2M field changed

I'm using `django-import-export` to bulk-update a model that has a `ManyToManyField`, with `skip_unchanged = True` set on the `Resource` so that rows that haven't actually changed don't generate updates.

Simplified setup:

```python
class Book(models.Model):
    name = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)

class BookResource(resources.ModelResource):
    class Meta:
        model = Book
        skip_unchanged = True
        report_skipped = True
```

I import an initial CSV, everything works. Later I import a second CSV where some books have a different set of categories than what's in the DB (e.g. a row's `categories` column changed from `Fiction` to `Fiction,Mystery`). I expect those rows to be imported as updates so the M2M relation gets rewritten.

What I actually see: those rows are reported as skipped. The non-M2M fields really are unchanged for those rows, but the M2M column in the CSV is clearly different from what's stored. After the import the `categories` relation in the DB is still the old value — no update happened.

If I turn `skip_unchanged` off, the same rows update correctly and the new categories show up in the DB, so the import itself can handle the change; it's just that with `skip_unchanged = True` the "did this row change?" check doesn't seem to notice changes that are confined to a `ManyToManyField`, and the row gets dropped before it would be saved.

Could the change-detection used by `skip_unchanged` take M2M fields into account so that rows whose only change is in a `ManyToManyField` are still imported?
