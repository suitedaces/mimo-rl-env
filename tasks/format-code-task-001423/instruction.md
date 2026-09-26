Creating a 2nd Captcha before the API scripts loads causes 2nd script to load
This is best explained by an example:

1. User is on Page A which has a Captcha A
2. Captcha A mounts, [putting an API script tag on the page](https://github.com/hCaptcha/react-hcaptcha/blob/master/src/index.js#L72).
3. User Navigates to Page B which has a Captcha B
4. Captcha B [resets the `captchaScriptCreated` flag](https://github.com/hCaptcha/react-hcaptcha/blob/master/src/index.js#L48-L51), then mounts which places another API script tag on the page.

This is most prevalent in scenarios where the user has a slow connection. I have also created a scenario to test this out there [here](https://codesandbox.io/s/react-hcaptchaform-example-invisible-forked-rlxmc?file=/src/Form.jsx).

## Expected Behavior
API script should only attempt to be loaded once.

## Current Behavior
API script is loaded more than once.

## Possible Solution
Remove the check from the constructor [here](https://github.com/hCaptcha/react-hcaptcha/blob/master/src/index.js#L48-L51), and instead update [this line](https://github.com/hCaptcha/react-hcaptcha/blob/master/src/index.js#L6) to be 
```js
const captchaScriptCreated = typeof hcaptcha !== 'undefined';
```

## Workaround
Load the script with a `<script>` tag before your page loads.
