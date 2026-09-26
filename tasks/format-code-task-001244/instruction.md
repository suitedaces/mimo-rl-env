## About section on the homepage shows raw template placeholders instead of real content

I cloned the repo to use it for our event and started the dev server. When I open the homepage, the **About** section is completely broken — instead of showing the section title, descriptions, button labels and the statistics (attendees / days / sessions / tracks numbers), the page literally renders the raw placeholder strings, e.g. you can read `{$ aboutBlock.title $}` and `{$ aboutBlock.statisticsBlock.attendees.number $}` etc. directly on the page where the actual text/numbers should appear.

The data does exist in `data/resources.json` under the `aboutBlock` key (title, callToAction, statisticsBlock, …), but the `about-block` component doesn't seem to be picking any of it up — every text node in that section just shows the placeholder source as plain text.

The same problem affects the "how it was" video button: clicking it opens the video dialog, but the dialog title is the literal placeholder string instead of the configured label, and I assume the YouTube id passed in is similarly broken (the video doesn't play correctly).

Other components on the page that read from `data/resources.json` render fine, so the JSON itself is loading — it looks like only `about-block` is affected. Could the about block be wired up so the values from the resources data actually show up in the rendered output?
