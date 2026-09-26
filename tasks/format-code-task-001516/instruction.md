CSP support for CSS Helper
### What is the feature you are proposing?

First of all, thanks a lot for you're awesome work on Hono. I really enjoy using it. 

I've been using the CSS helper. It works well 🚀 But in combination with nonce-based CSP i.e. if inline script and style tags are only allowed, if a random nonce is set on each render (e.g., `<style id="hono-css" nonce="1234">` or `<script nonce="1234">`, it doesn't work yet. Currently, there is no way to pass the nonce to the style and script tag. 

For example, I'd like to be able to add the nonce to the `<Style nonce="{c.get("secureHeadersNonce")}" />` to ensure the inline CSS is not ignored by the browser. 

For example, a test could look as follows:
```tsx
it('Should render CSS styles with CSP nonce', async () => {
  const headerClass = css`
    background-color: blue;
  `
  const template = (
    <>
      <Style nonce='1234' />
      <h1 class={headerClass}>Hello!</h1>
    </>
  )
  expect(await toString(template)).toBe(
    '<style id="hono-css" nonce="1234">.css-2458908649{background-color:blue}</style><h1 class="css-2458908649">Hello!</h1>'
  )
})
```

I'd like to help and contribute this feature and have started a possible implementation here: https://github.com/honojs/hono/pull/3685 -> happy for feedback! thanks!

### Related to 
- https://github.com/honojs/hono/pull/1858
- https://github.com/honojs/hono/pull/2577
