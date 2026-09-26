Roidmi Eva (roidmi.vacuum.v66) with genericmiot
**Describe the bug**
When I pass a command I have the following answer :

miiocli genericmiot --ip xxxxxxxx --token xxxxxxxx  status 
 Running command status
ERROR    Exception: 1 validation error for DeviceModel                                                      click_common.py:57
         services -> 1
           'NoneType' object is not iterable (type=type_error)
         Traceback (most recent call last):
           File "/usr/local/lib/python3.9/dist-packages/miio/click_common.py", line 55, in __call__
             return self.main(*args, **kwargs)
           File "/usr/local/lib/python3.9/dist-packages/click/core.py", line 1078, in main
             rv = self.invoke(ctx)
           File "/usr/local/lib/python3.9/dist-packages/click/core.py", line 1688, in invoke
             return _process_result(sub_ctx.command.invoke(sub_ctx))
           File "/usr/local/lib/python3.9/dist-packages/click/core.py", line 1688, in invoke
             return _process_result(sub_ctx.command.invoke(sub_ctx))
           File "/usr/local/lib/python3.9/dist-packages/click/core.py", line 1434, in invoke
             return ctx.invoke(self.callback, **ctx.params)
           File "/usr/local/lib/python3.9/dist-packages/click/core.py", line 783, in invoke
             return __callback(*args, **kwargs)
           File "/usr/local/lib/python3.9/dist-packages/miio/click_common.py", line 306, in wrap
             result = kwargs["result"] = func(*args, **kwargs)
           File "/usr/local/lib/python3.9/dist-packages/click/decorators.py", line 92, in new_func
             return ctx.invoke(f, obj, *args, **kwargs)
           File "/usr/local/lib/python3.9/dist-packages/click/core.py", line 783, in invoke
             return __callback(*args, **kwargs)
           File "/usr/local/lib/python3.9/dist-packages/miio/click_common.py", line 271, in
         command_callback
             return miio_command.call(miio_device, *args, **kwargs)
           File "/usr/local/lib/python3.9/dist-packages/miio/click_common.py", line 219, in call
             return method(*args, **kwargs)
           File "/usr/local/lib/python3.9/dist-packages/miio/click_common.py", line 186, in _wrap
             return func(self, *args, **kwargs)
           File "/usr/local/lib/python3.9/dist-packages/miio/integrations/genericmiot/genericmiot.py", line
         64, in status
             self._initialize_descriptors()
           File "/usr/local/lib/python3.9/dist-packages/miio/integrations/genericmiot/genericmiot.py", line
         143, in _initialize_descriptors
             self.initialize_model()
           File "/usr/local/lib/python3.9/dist-packages/miio/integrations/genericmiot/genericmiot.py", line
         56, in initialize_model
             self._miot_model = miotcloud.get_device_model(self.model)
           File "/usr/local/lib/python3.9/dist-packages/miio/miot_cloud.py", line 90, in get_device_model
             return DeviceModel.parse_obj(spec)
           File "/usr/local/lib/python3.9/dist-packages/pydantic/v1/main.py", line 526, in parse_obj
             return cls(**obj)
           File "/usr/local/lib/python3.9/dist-packages/miio/miot_models.py", line 456, in __init__
             super().__init__(*args, **kwargs)
           File "/usr/local/lib/python3.9/dist-packages/pydantic/v1/main.py", line 341, in __init__
             raise validation_error
         pydantic.v1.error_wrappers.ValidationError: 1 validation error for DeviceModel
         services -> 1
           'NoneType' object is not iterable (type=type_error)

Maybe because there is 4 version of the roidmi v66?

**Version information (please complete the following information):**
 - OS: Debian 11
 - python-miio:  miiocli, version 0.6.0.dev0

**Device information:**
Model: roidmi.vacuum.v66
Hardware version: Linux
Firmware version: 1.4.6_3271
Supported using: GenericMiot
Supported by genericmiot: True

**To Reproduce**
Steps to reproduce the behavior:
1. Execute the command : miiocli genericmiot --ip xxxxxxxx --token xxxxxxxx  status
