I'm writing a plugin and want my own store that just lets consumers subscribe via addChangeListener, but the only BaseStore I can see in the codebase comes bundled with this get/set thing that auto-dispatches APP_STORE_CHANGE through PluginSDK — which I really don't want my plugin store doing.

Could we expose a lean BaseStore through PluginSDK that's basically just the change-listener part, and keep the get/set+dispatch behavior as a separate thing for stores that actually need it?

Would make it way easier to build plugin-side stores without inheriting the whole app-store machinery.
