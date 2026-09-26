Extended color theme can't down to level three.
Please see this minimum example

In this [Tailwind Play](https://play.tailwindcss.com/HF8x5A6SqK) I created, the color theme can be extended down to three-level like this

## Normal Tailwind

```js
module.exports = {
  theme: {
    extend: {
      colors: {
        v2: {
          red: {
            500: '#DC2626',
          },
        },
      },
    },
  },
}
```

```html
<div class="text-v2-red-500">Three level custom color</div>
```

Result:

![image](https://user-images.githubusercontent.com/7580792/103261935-47bbf600-49de-11eb-85ba-692059c02576.png)

However, in twind, it's not working, and typing yells also

[Codesandbox](https://codesandbox.io/s/extended-color-theme-cant-down-to-level-three-s7xnl?file=/src/index.ts)

Result:

![image](https://user-images.githubusercontent.com/7580792/103261998-85b91a00-49de-11eb-8179-8211835dbc8b.png)
