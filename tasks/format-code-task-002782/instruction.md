### Describe the bug

click on migrate in the reproduction link, see the compile error for snippet default.

```html
<Component><div slot="default">default slot</div></Component>
```

gets turned into

```html
<Component>{#snippet default()}<div >default slot</div>{/snippet}</Component>
```

but should be 

```html
<Component>{#snippet children()}<div >default slot</div>{/snippet}</Component>
```

workaround, find and replace `slot="default"` with an empty string in your .svelte files before running the migration or find and replace `#snippet default` with `#snippet children`

### Reproduction

https://svelte-omnisite.vercel.app/playground/hello-world?version=5.0.0-next.272#H4sIAAAAAAAAA3VP0QqDMAz8lZIXX0TfXS2Mfca6B6cRCjUtbXQb4r8PRRSHe0pyl9zlRmiNxQjFfQT-eIRiASAFqrp5unqfxQEtz9iziniG144YiSMUIGMdjGelSbPpvAssbq7zjpBYtMF1IsnyDVklknnbIotZXJQieblgm-SiSea7HsntTsnGDCJax6WGBtuqt6xBrd1CyLwxg5K7l9IEKTC-GQoOPU7pn8i_3x2Dn7CH-NaxkvlSjnaP6QvENl3YbQEAAA==

### Logs

```shell
default is a reserved word
```


### System Info

```shell
playgroun
```


### Severity

annoyance
