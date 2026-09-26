## `googlefonts/article/images` should report missing image files as a blocking error, not a warning

I maintain a font family for Google Fonts and recently shipped an `article/ARTICLE.en_us.html` along with the font. The HTML references a couple of images under `article/images/` via `<img src="...">` tags. I renamed one of the image files and forgot to update the corresponding `src` in the HTML.

When I ran fontbakery's Google Fonts profile to validate the family before submitting, the `googlefonts/article/images` check did flag the broken reference — but only as a **WARN** under the `missing-visual-file` message. I almost missed it among the other warnings and was about to submit the family. If it had gone through, the article page on the Google Fonts site would have rendered with a broken image placeholder.

A missing image file referenced from the article HTML isn't a "nice to fix" issue — it's a guaranteed visual breakage on the published page. WARN is too easy to skim past, and there's no way to argue this is acceptable to ship. The check should report missing image files at the most severe level so that it's treated as a hard blocker, on par with other issues that genuinely prevent shipping. Right now it sits at the same level as cosmetic suggestions, which doesn't reflect the actual impact.

Please bump the severity of `missing-visual-file` in the `googlefonts/article/images` check accordingly.
