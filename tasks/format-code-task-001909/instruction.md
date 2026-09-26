## `TabInfo` renders an empty `<div>` when there's nothing to show

While working on some styling in the details view, I noticed that the `TabInfo` component always renders a wrapper `<div>` in the DOM, even when there is no message to display (i.e. when the target page is not hidden). So in the common case I end up with a stray empty `<div></div>` sitting in the tree.

When the component has nothing to show, it should render `null` instead of an empty container — same visible behavior, but it keeps the DOM clean and avoids surprises when adding styles to surrounding elements.
