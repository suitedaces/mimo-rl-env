Using convertToHTML returning an <img> tag in blockToHTML gives error
I get the following error when I try to use `draft-convert` convertToHTML returning an `<img>` tag in blockToHTML gives error

```
Uncaught Error: img is a void element tag and must neither have 'children' nor use 'dangerouslySetInnerHTML'
```

Here is my function for exporting to html.

```jsx
export function editorStateToHtml (editorState) {
  if (editorState) {
    const html = convertToHTML({
      styleToHTML: (style) => {
        if (style === 'BOLD') {
          return <span style={{color: 'blue'}} />;
        }
      },
      blockToHTML: (block) => {
        const type = block.type
        if (type === 'atomic') {
          let url = block.data.src
          return <img src={url} />
        }
        if (type === 'unstyled') {
          return <p />
        }
      },
      entityToHTML: (entity, originalText) => {
        if (entity.type === 'LINK') {
          return <a href={entity.data.url}>{originalText}</a>;
        }
        return originalText;
      }
    })(editorState.getCurrentContent());

    return html
  }
}
```
