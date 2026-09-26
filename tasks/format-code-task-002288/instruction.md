PageWaitForRequestOptions and PageWaitForResponseOptions are not used anywhere
The above mentioned types don't seem to be used in their respective function calls (WaitForRequest and WaitForResponse).

Looking at the code [here](https://github.com/mxschmitt/playwright-go/blob/de638a4c485a9853c489991f51d3463a9ece7126/page.go#L336) confirms that there is no way to set the timeout for those methods (other than setting the default page timeout).
