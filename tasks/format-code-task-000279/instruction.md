# Split the review workflow into source and translation reviews

Right now a project has a single switch that turns the review workflow on or off
for everything. We want finer control: reviewing **source strings** should be
configurable independently from reviewing **translations**.

Please give a project two independent boolean on/off settings:

* `source_review` — enables the review workflow for source strings, and
* `translation_review` — enables the review workflow for translations.

Both must default to **off** (`False`) for newly created projects.

A lot of the codebase needs to know "is review in effect for *this* translation?".
Make that easy to ask directly on a translation through a boolean
`enable_review` attribute: it must report the project's `source_review` setting
for a translation that holds the source strings, and the project's
`translation_review` setting for every other translation.

Wire the rest of the review machinery to the new settings instead of one
project-wide flag:

* **The `unit.review` permission.** When the object being checked is a
  translation, the permission may only be granted when review is enabled for
  that particular translation (on top of the user actually being allowed to
  review). When the object being checked is a whole component or project, the
  enablement gate is satisfied as long as *either* review type is enabled on the
  project.

* **Approved state.** A unit may only settle into the *approved* state when
  review is enabled for the translation it belongs to — a source unit needs
  source review, any other unit needs translation review. With the relevant
  review type disabled, a unit that would otherwise be approved must instead be
  treated as merely translated.

* **The per-project "Review" access-control group.** This group should be
  created only when at least one of the two review types is enabled for the
  project; when both are disabled it must not be created.

The existing single-flag behavior should be fully replaced by the two new
settings.
