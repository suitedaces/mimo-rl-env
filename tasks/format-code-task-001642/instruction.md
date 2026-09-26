Round-Robin GPU scheduling does not follow CUDA_VISIBLE_DEVICES spec
**Describe the bug**

`CUDA_VISIBLE_DEVICES: "RR1,3,5,7"` works, but

`CUDA_VISIBLE_DEVICES: "RRGPU-0aaaaaaa-74d2-7297-d557-12771b6a79d5,GPU-0bbbbbbb-74d2-7297-d557-12771b6a79d5,GPU-0ccccccc-74d2-7297-d557-12771b6a79d5,GPU-0ddddddd-74d2-7297-d557-12771b6a79d5"` does NOT work, but should work

The GPU UUIDs (visible with `nvidia-smi -L`) should be drop-in replacements for numeric IDs.

I prefer to use UUIDs because they are more deterministic (reliable) when environments and cards are moved between systems.

**Describe how you solve it**

I currently use numeric IDs, but those are unreliable as I move GPUs around often.

---

<!-- Optional, but really help us locate the problem faster -->

**Environment**
```
- jina 3.8.3
- docarray 0.16.2
- jcloud 0.0.35
- jina-hubble-sdk 0.18.0
- jina-proto 0.1.13
- protobuf 3.20.1
- proto-backend cpp
- grpcio 1.47.0
- pyyaml 6.0
- python 3.8.10
- platform Linux
- platform-release 5.15.0-52-generic
- platform-version jina-ai/jina#58-Ubuntu SMP Thu Oct 13 08:03:55 UTC 2022
- architecture x86_64
- processor x86_64
- uid 2485377892357
- session-id fcbedcc8-5d43-11ed-9251-0242ac110005
- uptime 2022-11-05T19:56:49.977485
- ci-vendor (unset)
* JINA_DEFAULT_HOST (unset)
* JINA_DEFAULT_TIMEOUT_CTRL (unset)
* JINA_DEPLOYMENT_NAME (unset)
* JINA_DISABLE_UVLOOP (unset)
* JINA_EARLY_STOP (unset)
* JINA_FULL_CLI (unset)
* JINA_GATEWAY_IMAGE (unset)
* JINA_GRPC_RECV_BYTES (unset)
* JINA_GRPC_SEND_BYTES (unset)
* JINA_HUB_NO_IMAGE_REBUILD (unset)
* JINA_LOG_CONFIG (unset)
* JINA_LOG_LEVEL (unset)
* JINA_LOG_NO_COLOR (unset)
* JINA_MP_START_METHOD (unset)
* JINA_OPTOUT_TELEMETRY (unset)
* JINA_RANDOM_PORT_MAX (unset)
* JINA_RANDOM_PORT_MIN (unset)
```

**Screenshots**
N/A
