### Describe the bug
Panic occured randomly in one of our microservices.

```
panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x1 addr=0x8 pc=0xe01628]

goroutine 327 [running]:
github.com/fsnotify/fsnotify.(*watches).remove(0xc0007bdec0, 0x90de68?)
        /go/pkg/mod/github.com/fsnotify/fsnotify@v1.7.0/backend_inotify.go:182 +0x88
github.com/fsnotify/fsnotify.(*Watcher).readEvents(0xc00012cd00)
        /go/pkg/mod/github.com/fsnotify/fsnotify@v1.7.0/backend_inotify.go:535 +0x4a5
created by github.com/fsnotify/fsnotify.NewBufferedWatcher
        /go/pkg/mod/github.com/fsnotify/fsnotify@v1.7.0/backend_inotify.go:270 +0x1f0
```

### Code to Reproduce

Not able to reproduce

### File operations to reproduce

NA

### Which operating system and version are you using?

Linux 6.1.58+ SMP PREEMPT_DYNAMIC Mon Jan 29 15:19:25 UTC 2024 x86_64 Linux

### Which fsnotify version are you using?

v1.7.0

### Did you try the latest main branch?

No
