## `Toc` only renders 2 levels of nesting

I'm building a docs sidebar with `<Toc>` from `@gravity-ui/uikit`. My table of contents is naturally a tree — chapters contain sections, sections contain subsections, and so on — so I pass that whole tree into `items`, using the nested `items` field on each entry:

```tsx
<Toc
    value={active}
    onUpdate={setActive}
    items={[
        {
            value: 'disk',
            content: 'Disk',
            items: [
                {
                    value: 'control',
                    content: 'Disk controls',
                    items: [
                        {value: 'floppy', content: 'Floppy'},
                        {value: 'hard',   content: 'Hard'},
                    ],
                },
                {
                    value: 'snapshots',
                    content: 'Disk snapshots',
                    items: [
                        {value: 'standard', content: 'Standard'},
                    ],
                },
            ],
        },
        // ...
    ]}
/>
```

What I actually see in the rendered TOC is just the first two levels: `Disk`, and under it `Disk controls` / `Disk snapshots`. Everything from the third level down (`Floppy`, `Hard`, `Standard`, …) is silently dropped — no warning, nothing in the DOM. As far as I can tell from the type, nested `items` are supposed to be supported at any depth, so this looks like a bug rather than intended behavior.

It would be great if `Toc` actually walked the tree and rendered nested entries down to a reasonable depth (something like 5–6 levels should comfortably cover real docs).

Related: even in the 2-level version that works today, the indentation of nested items is fixed — every child is offset by the same amount regardless of how deep it is. Once deeper levels render, they should also be visually distinguishable, i.e. each additional level should be indented a bit further than its parent, so you can tell the hierarchy apart just by looking.
