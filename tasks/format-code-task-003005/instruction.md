Show fan speed
Command `nvidia-smi` shows also fan speed:

```bash
$ nvidia-smi
Wed Apr  3 14:09:10 2019
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 396.37                 Driver Version: 396.37                    |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  GeForce GTX 108...  On   | 00000000:03:00.0  On |                  N/A |
| 30%   42C    P8    16W / 250W |     53MiB / 11177MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
|   1  GeForce GTX 108...  On   | 00000000:04:00.0 Off |                  N/A |
| 31%   43C    P8    16W / 250W |      2MiB / 11178MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
|   2  GeForce GTX 108...  On   | 00000000:81:00.0 Off |                  N/A |
| 51%   68C    P2    76W / 250W |  10781MiB / 11178MiB |     17%      Default |
+-------------------------------+----------------------+----------------------+
|   3  GeForce GTX 108...  On   | 00000000:82:00.0 Off |                  N/A |
| 29%   34C    P8    16W / 250W |      2MiB / 11178MiB |      0%      Default |
```

Could gpustat show this information too?
