Use agreed LeadingStory layouts
**Is your feature request related to a problem? Please describe.**
Following discussion with UX, we have updated the layouts for `StoryPromo`s of type `'leading'`.

**Describe the solution you'd like**
On all breakpoints, the DOM ordering will be `Info` component (containing Headline, Summary, Timestamp) followed by the `Image` component. Internally this means the `TextGridItem` followed by `ImageGridItem`.

| Breakpoint | `TextGridItem` columns | `ImageGridItem` columns | Total columns/line |
|------------|-------------------------|---------------------------|-------------------|
| > 1007px | 2 | 4 | 6 |
| 600px - 1007px | 3 | 3 | 6 |
| < 600px | 6 | 6 | 6 |

This will also need the relevant fallbacks added.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Testing notes**
[Tester to complete]

Dev insight: Will there be any potential regression? etc

- [x] This feature is expected to need manual testing.

**Additional context**
Tablet: 
![image](https://user-images.githubusercontent.com/43134742/73276695-ff4df400-41e0-11ea-876e-31091df336d5.png)

Mobile (note the padding under the timestamp is not correct, this was a quick prototype):
![image](https://user-images.githubusercontent.com/43134742/73276441-99fa0300-41e0-11ea-921a-5ed36d04bcd2.png)
