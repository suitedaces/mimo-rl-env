[icon] Custom preserveAspectRatio attribute value on the icon is not respected
### Description

Similar to #3992 but for `preserveAspectRatio`

Currently, the `vaadin-iconset` does not take custom `preserveAspectRatio` into account.

### Expected outcome

The attribute on the `<g>` element with an `id` attribute should be respected.

### Minimal reproducible example

```html
<script type="module">
  import '@vaadin/icon';
  import { Iconset } from '@vaadin/icon/vaadin-iconset.js';

  const template = document.createElement('template');
  template.innerHTML = `
    <svg xmlns="http://www.w3.org/2000/svg">
      <defs>
        <svg
          id="my-icons-iconset:logo"
          xmlns="http://www.w3.org/2000/svg"
          width="32"
          height="26"
          preserveAspectRatio="xMidYMin slice"
        >
          <g fill="#770C56" fill-rule="evenodd">
            <path d="M.077 12.962c0-2.496.464-4.85 1.392-7.062A17.772 17.772 0 0 1 5.48.023h3.508C5.349 3.583 3.53 7.896 3.53 12.962c0 5.065 1.819 9.378 5.457 12.939H5.479a17.772 17.772 0 0 1-4.01-5.878C.541 17.812.077 15.458.077 12.962zm31.36 0c0 2.496-.463 4.85-1.391 7.061a17.772 17.772 0 0 1-4.01 5.878h-3.508c3.638-3.56 5.457-7.874 5.457-12.94 0-5.065-1.819-9.378-5.457-12.938h3.509A17.772 17.772 0 0 1 30.046 5.9c.928 2.212 1.392 4.566 1.392 7.062zM12.954 1.721h2.32v13.191h-2.32z"/><path d="m15.273 14.871-1.504-1.487 9.434-9.328 1.503 1.487-9.433 9.328z"/>
          </g>
        </svg>
      </defs>
    </svg>
  `;

  Iconset.register('my-icons-iconset', 32, template);
</script>

<vaadin-icon icon="my-icons-iconset:logo"></vaadin-icon>

```

### Steps to reproduce

1. Add the example above to the HTML page (using dev pages)
2. Open the page and observe the attribute value in dev tools

<img width="804" alt="Screenshot 2023-05-15 at 15 58 51" src="https://github.com/vaadin/web-components/assets/10589913/82d3a44d-a574-44c7-bf4c-2d11134256d7">

### Environment

Vaadin version(s): 23.3, 24.0, 24.1

### Browsers

Issue is not browser related
