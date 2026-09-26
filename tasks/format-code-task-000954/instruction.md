[dotprompt] Allow for synchronous references to prompt files.
At the moment, `prompt` is an async function that loads a prompt from the registry. This is in practice annoying because most of the time you want a prompt to be a high-level reference that is registered at the top level:

```ts
const myPrompt = prompt("myPrompt");

const myFlow = defineFlow({...}, input => {
  const result = myPrompt.generate(...);
});
```

Since top-level await is bad, this desirable pattern is not currently possible.

### Proposal: PromptRef

Instead of `prompt` async returning a `Dotprompt` class, it can instead return a memoizing proxy ref, something like:

```ts
class DotpromptRef {
  name: string;
  private _prompt: Dotprompt;
  constructor(name: string) {
    this.name = name;
    this.loadPrompt(name);
  }

  private async loadPrompt(): Dotprompt {
    if (this._prompt) return this._prompt;
    this._prompt = await lookupPrompt(...);
    return this._prompt;
  }

  async generate(...) {
    return (await this.loadPrompt()).generate(...);
  }
  async render(...) { ... }
}
```

This way, a prompt reference can be loaded synchronously while still working exactly the same as the async version today in practice.
