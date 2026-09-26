# Namespace-aware file attachments for publications

On the publication feed, people can now attach files both to a publication and to the
comments below it. Content that is created from the publication area lives under its own
"publication" content namespace, which is distinct from the regular "upload" area and from
ordinary "content". Our shared frontend library (`tracim_frontend_lib`) currently has no notion
of these namespaces, so a couple of pieces need to grow that awareness.

Please make the following changes in the shared library, exposed through its public API:

1. **Expose the set of content namespaces.** Add a `CONTENT_NAMESPACE` enumeration to the
   library's public exports describing the three namespaces the backend understands:
   - `CONTENT` → `"content"`
   - `UPLOAD` → `"upload"`
   - `PUBLICATION` → `"publication"`

2. **Fetch only the relevant file children.** The helper that retrieves the file children of a
   content (`getFileChildContent(apiUrl, workspaceId, contentId)`) must restrict its results to
   the *content* and *publication* namespaces, so that files sitting in the general upload area
   are not returned. This is in addition to the existing filtering it already performs (by parent
   id and by the `file` content type), and the request must remain a `GET`.

3. **Remember the namespace of queued comment files.** The app-content factory provides a method
   for queuing files that will later be sent as comments. Today it takes the list of files to
   queue and a state setter. Extend it so the caller also passes the content namespace those files
   belong to — the new argument comes after the file list and before the state setter. Every file
   that gets newly queued must record that namespace under a `namespace` field on the queued entry
   (so it can later be uploaded into the right namespace). The existing behavior must be preserved:
   files whose name already appears in the pending list are skipped, the remaining files are
   appended to what is already queued, and an empty input list is a no-op.
