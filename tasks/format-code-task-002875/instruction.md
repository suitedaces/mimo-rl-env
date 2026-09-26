# Attach files to comments in the timeline

Our app components (file, html-document, thread, …) are all wrapped by a shared
higher-order "app content factory" that injects the helpers they use to manage
the comment area and to build the content timeline. Today users can only post a
textual comment. We want them to be able to attach files to a content's timeline
the same way comments are attached, so the shared factory needs to support this
end to end.

### Staged attachments

The factory must inject two new handlers that an app component uses to manage the
files a user has staged but not yet sent. The staged files live in the wrapped
component's state under `newCommentAsFileList`; each entry is an object that
exposes a `file` with a `name`.

* `appContentAddCommentAsFile(fileList, setState)` appends the given entries to
  the staged list, but it never adds an entry whose `file.name` is already staged
  (de-duplicate by name). Adding an empty list changes nothing.
* `appContentRemoveCommentAsFile(fileToRemove, setState)` removes the staged entry
  whose `file.name` equals `fileToRemove.file.name`. A falsy `fileToRemove`
  changes nothing.

Both handlers must derive the new staged list from its previous value, so that
repeated adds accumulate and earlier entries are never dropped.

### Building the timeline

The timeline must now show attached files alongside comments and revisions.
`buildTimelineFromCommentAndRevision` should additionally accept the list of file
contents that were attached to the content, passed as an extra argument placed
immediately after the comment list (so the order becomes comment list, attached
file list, revision list, logged user, optional initial translation state).

The result is a single flat list containing every comment, every attached file,
and every revision, ordered chronologically by creation time, oldest first. Every
item keeps its raw creation timestamp and gains a humanized creation label.
Attached-file items must be tagged with a timeline item type that is distinct from
both the comment type and the revision type, so the UI can render them
differently.

### Live updates

`addCommentToTimeline`, which appends a freshly created content to an existing
timeline, must also handle file contents: when the incoming content is a file
rather than a comment it is inserted as an attached-file item (with that same
distinct type) instead of as a comment item, and the returned timeline stays
ordered chronologically.
