### Environment

------------------------------
- Operating System: Linux
- Node Version:     v20.18.0
- Nuxt Version:     3.15.0
- CLI Version:      3.17.2
- Nitro Version:    2.10.4
- Package Manager:  pnpm@9.15.1
- Builder:          -
- User Config:      default
- Runtime Modules:  -
- Build Modules:    -
------------------------------

### Reproduction

https://github.com/jianxing-xu/reproduction_env

### Describe the bug

updating .env file, after refresh and check coonsole log, value unchanged

### Additional context

/api111112112321
ℹ .env changed, restarting server...                                                                                                                                                                                 9:15:38 AM

 ERROR  [unhandledRejection] connect ECONNREFUSED 127.0.0.1:46551                                                                                                                                                     9:15:38 AM

    at TCPConnectWrap.afterConnect [as oncomplete] (node:net:1607:16)

  ➜ DevTools: press Shift + Alt + D in the browser (v1.7.0)                                                                                                                                                           9:15:39 AM

✔ Vite client built in 32ms                                                                                                                                                                                          9:15:40 AM
✔ Vite server built in 414ms                                                                                                                                                                                         9:15:41 AM
✔ Nuxt Nitro server built in 701 ms                                                                                                                                                                            nitro 9:15:42 AM
ℹ Vite client warmed up in 2ms                                                                                                                                                                                       9:15:42 AM
ℹ Vite server warmed up in 537ms                                                                                                                                                                                     9:15:42 AM
/api111112112321


/**.env file**/
NUXT_PUBLIC_API_BASE=/api

### Logs

```shell-script

```
