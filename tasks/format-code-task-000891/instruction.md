5.1.0 - Each then() should return a value or throw
Updated deps this morning. In particular, eslint-plugin-promise from v4.3.1 to v5.1.0 (did you forget to make a tag for this release?) and getting the following error:

```
error  Each then() should return a value or throw  promise/always-return
```

The code in question looks like this:

```js
export const fetchAbout = async function ({ commit, state, getters, rootState }) {
  return axios.get(state.baseUrl)
    .then((results) => {
      if (results.status === 200) { // OK
        commit('setAbout', results.data.payload)
        return results
      }
      else {
        throw new Error(results.data.error || results.data)
      }
    })
    .catch(function (error) {
      console.error('fetch about', error)
      throw error
    })
}
```

I am not seeing the issue here. There is both a `return` and a `throw` involved.
**Expected behavior:** No error here

**Actual behavior:** issues an error

### Versions

- Node version: v12.18.4
- ESLint version: v7.23.0
- eslint-plugin-promise version: v5.1.0
