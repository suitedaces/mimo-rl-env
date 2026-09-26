The text, below element, should not be capitalized as it changes meaning completely
### Expected behavior
When Taiko executes the text should display
```
Wrote BR3 4AS into the textBox below element with text Postcode
```

### Actual behavior
1. When Taiko executes the text should display
```
Wrote BR3 4AS into the textBox Below Element with text Postcode
```
2. The text **below element** should not be capitalized as it changes meaning completely.

### Steps to reproduce
1. Execute the script [Taiko-BT-Headless.js](https://github.com/amitsarkar007/Taiko-Scripts/blob/master/Taiko-BT-Headless.js)
2. Check the terminal for the output
```
taiko .\Taiko-BT-Headless.js
[PASS] Browser opened
[PASS] Navigated to URL http://bt.com
[PASS] Clicked element matching text "OK" 1 times
[PASS] Clicked element matching text "Broadband" 1 times
[PASS] Clicked element matching text "Fibre broadband" 1 times
[PASS] Clicked element matching text "See broadband deals" 1 times
[PASS] Clicked element matching text "Add and continue" 1 times
[PASS] Wrote BR3 4AS into the textBox Below Element with text Postcode 
[PASS] Clicked element matching text "Check availability" 1 times
[PASS] Clicked button with label 55 Eden Road  1 times
[PASS] Clicked element matching text "Confirm address" 1 times
[PASS] Browser closed
```

### Versions
```
taiko --version
Version: 1.0.16 (Chromium: 85.0.4168.0) RELEASE

node --version
v12.18.3
```
