## Cannot delete an extended form that implements an interface

I added an extended form to my data model that implements one of the existing model interfaces (so it inherits a few props from that interface automatically — I didn't define those props myself on the form). Later I wanted to remove the form from the model, but the delete is rejected:

```
Form has extended properties: <prop1>, <prop2>, ...
```

The properties it lists in that error are exactly the ones that came in through the interface — I never added any extended properties of my own on this form. As far as I'm concerned the form is "clean" from the user's point of view; the only props attached to it are the ones the interface contributed.

This makes any extended form that implements an interface effectively undeletable, which seems wrong. Inherited interface props should follow the interface, not count as user-added extended props that block removing the form.

Could `delForm` be fixed so a form like this can actually be removed?
