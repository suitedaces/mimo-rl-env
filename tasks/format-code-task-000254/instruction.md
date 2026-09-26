## MagdaReference items don't inherit `accessType` from a private parent group

I have a catalog where I'm grouping a few `MagdaReference` items under a parent group that I've configured as private (using `AccessControlMixin`'s `setAccessType("private")` on the group). My expectation, based on how every other catalog item behaves, is that the children should inherit the parent's access type when they don't have explicit access info of their own — so the magda items under a private group should also show up as private in the UI.

What actually happens is that those `MagdaReference` children are reported as **public**, even when their parent is clearly private. As a result the workbench / catalog UI flags them as public alongside genuinely public items, which is misleading for the people we're sharing the catalog with.

To convince myself it isn't a problem with the parent or the mixin itself, I swapped one of the magda children for a regular catalog item under the same parent group — that one correctly comes through as private. So the parent inheritance machinery itself is working; it's specifically `MagdaReference` that disagrees.

The behaviour seems to depend on whether the underlying Magda record has been populated yet:

- Once the magda record is loaded and it carries access-control info, `accessType` does the right thing (public vs. non-public based on that record).
- But before the record is loaded, or for any `MagdaReference` where the record info isn't there, `accessType` always comes out as `"public"` regardless of the surrounding catalog structure. `isPublic` is `true` and `isPrivate` is `false` even though the containing group is private.

I'd expect `MagdaReference` to fall back to the same default access-type resolution that every other `AccessControlMixin` consumer uses — i.e. honour explicit settings, then look at the referrer / ancestors — whenever it doesn't have its own access info from a Magda record. Hard-coding `"public"` in that fallback path means a private subtree silently exposes public-looking children in the UI.
