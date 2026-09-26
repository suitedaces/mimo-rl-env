SmartTub integration Failed to parse fullStatus response
### The problem

I installed the SmartTub integration and it connected to my SmartTub cloud account, but all I get is Unknown for all status in the integration.  From the log:
`Logger: smarttub.api
Source: runner.py:186
First occurred: October 16, 2023 at 3:14:45 PM (3932 occurrences)
Last logged: 8:57:00 AM

Failed to parse fullStatus response: {'ambientTemperature': None, 'blowoutCycle': None, 'cleanupCycle': 'INACTIVE', 'date': None, 'demoMode': 'DISABLED', 'dipSwitches': 2, 'displayTemperatureFormat': 'FAHRENHEIT', 'errorCode': 0, 'error': {'code': 0, 'title': 'All Clear', 'description': None}, 'flowSwitch': None, 'heater': 'OFF', 'heatMode': 'READY', 'highTemperatureLimit': None, 'lastUpdated': '2023-10-19T14:06:35.499Z', 'state': 'INIT', 'ozone': 'OFF', 'setTemperature': 38.9, 'time': '00:06:00', 'timeFormat': 'HOURS_12', 'timezone': None, 'uv': 'OFF', 'uvOnDemand': 'OFF', 'current': {'value': 0.0, 'min': 0.0, 'max': 0.0, 'average': 0.0, 'kwh': 0.411}, 'primaryFiltration': {'mode': 'NORMAL', 'status': 'INACTIVE', 'startHour': 20, 'duration': 4, 'cycle': 0, 'startMinute': 0, 'durationMinute': 0, 'lastUpdated': '2023-10-19T07:06:26.871Z'}, 'secondaryFiltration': {'mode': 'AWAY', 'status': 'INACTIVE', 'enabled': True, 'startHour': 8, 'startMinute': 0, 'durationHour': 4, 'durationMinute': 0, 'lastUpdated': '2023-10-19T07:06:26.871Z'}, 'water': {'oxidationReductionPotential': None, 'ph': None, 'temperature': 39.4, 'turbidity': None, 'temperatureLastUpdated': '2023-10-19T13:23:05.013Z'}, 'versions': {'balboa': '1.09', 'controller': '62.00', 'jacuzziLink': '81'}, 'locks': {'temperature': 'UNLOCKED', 'spa': 'UNLOCKED', 'access': 'UNLOCKED', 'maintenance': 'UNLOCKED'}, 'location': {'latitude': 47.7516708, 'longitude': -121.9901199, 'accuracy': 3010.0}, 'fieldsLastUpdated': {'heatMode': '2023-10-19T07:06:26.871Z', 'setTemperature': '2023-10-19T07:06:26.871Z', 'uv': '2023-10-19T07:06:26.871Z', 'uvOnDemand': '2023-10-19T07:06:26.871Z', 'online': None, 'errEvent': '2023-10-12T00:26:08.512Z', 'locEvent': '2023-10-17T01:48:20.524Z', 'rpstEvent': '2023-10-19T13:25:20.286Z', 'spstEvent': '2023-10-19T14:06:35.356Z', 'cfstEvent': '2023-10-19T07:06:24.156Z', 'sp2stEvent': '2023-10-19T07:06:25.676Z', 'wcstEvent': None}, 'watercare': None, 'online': None, 'pumps': [{'id': 'P2', 'type': 'JET', 'state': 'OFF', 'speed': 'ONE_SPEED', 'current': None}, {'id': 'P1', 'type': 'JET', 'state': 'OFF', 'speed': 'TWO_SPEED', 'current': None}], 'lights': [{'zone': 1, 'mode': 'ON', 'cycleSpeed': 0, 'color': {'red': 0, 'blue': 0, 'green': 0, 'white': 0}, 'intensity': 0, 'irt': None, 'exterior': False}], 'sensors': [], 'lowRangeLowTemp': 65, 'lowRangeHighTemp': 99, 'highRangeLowTemp': 80, 'highRangeHighTemp': 104, 'tempRange': 'HIGH', 'heater1Present': 'PRESENT', 'heater2Present': 'NOT_PRESENT', 'ozoneSystemPresent': 'NOT_PRESENT', 'primingMode': 'INACTIVE', 'heater2On': 'OFF', 'heatPumpStatus': 'NOT_PRESENT', 'heatPumpMode': 'DISABLED', 'heatPumpEfficiency': 'AUTO_SMART', 'electricHeaterMode': 'M7', 'czStatus': 'NOT_PRESENT', 'chromazon3Present': 'OFF', 'chromazon3Zone1': 'FULL_CONTROL', 'chromazon3Zone2': 'FULL_CONTROL', 'chromazon3Zone3': 'FULL_CONTROL', 'heatCanWait': 4, 'heatVacation': False, 'signal': {'strength': 12, 'quality': 6, 'signalAt': None, 'country': 'US', 'updateAt': '2023-10-19T11:45:54.049Z'}, 'errors': [], 'timeSet': None}`

From the Update Coordinator:
`Logger: homeassistant.components.smarttub.controller
Source: helpers/update_coordinator.py:290
Integration: SmartTub ([documentation](https://www.home-assistant.io/integrations/smarttub), [issues](https://github.com/home-assistant/core/issues?q=is%3Aissue+is%3Aopen+label%3A%22integration%3A+smarttub%22))
First occurred: October 16, 2023 at 3:14:45 PM (3932 occurrences)
Last logged: 8:57:00 AM

Unexpected error fetching smarttub data: None
Traceback (most recent call last):
  File "/usr/src/homeassistant/homeassistant/helpers/update_coordinator.py", line 290, in _async_refresh
    self.data = await self._async_update_data()
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/src/homeassistant/homeassistant/helpers/update_coordinator.py", line 246, in _async_update_data
    return await self.update_method()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/src/homeassistant/homeassistant/components/smarttub/controller.py", line 89, in async_update_data
    data[spa.id] = await self._get_spa_data(spa)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/src/homeassistant/homeassistant/components/smarttub/controller.py", line 96, in _get_spa_data
    full_status, reminders, errors = await asyncio.gather(
                                     ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/smarttub/api.py", line 215, in get_status_full
    return SpaStateFull(self, full_status)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/smarttub/api.py", line 352, in __init__
    super().__init__(spa, **state)
  File "/usr/local/lib/python3.11/site-packages/smarttub/api.py", line 280, in __init__
    self._prop("blowoutCycle", constructor=lambda x: self.CycleStatus[x])
  File "/usr/local/lib/python3.11/site-packages/smarttub/api.py", line 341, in _prop
    self, instance_variable_name, constructor(self.properties[json_key])
                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.11/site-packages/smarttub/api.py", line 280, in <lambda>
    self._prop("blowoutCycle", constructor=lambda x: self.CycleStatus[x])
                                                     ~~~~~~~~~~~~~~~~^^^
  File "/usr/local/lib/python3.11/enum.py", line 790, in __getitem__
    return cls._member_map_[name]
           ~~~~~~~~~~~~~~~~^^^^^^
KeyError: None`

### What version of Home Assistant Core has the issue?

core-2023.10.3

### What was the last working version of Home Assistant Core?

_No response_

### What type of installation are you running?

Home Assistant OS

### Integration causing the issue

SmartTub

### Link to integration documentation on our website

https://www.home-assistant.io/integrations/smarttub

### Diagnostics information

SmartTub doesn't provide diagnostic data.   Here's the core log:
`2023-10-19 09:05:45.434 DEBUG (MainThread) [smarttub.api] login successful, username=XXXXXXXXXXXXXXXXX
2023-10-19 09:05:45.668 DEBUG (MainThread) [smarttub.api] GET accounts/XXXXXXXXXX successful: {'id': 'XXXXXXXXXX ', 'email': 'XXXXXXXXXXXXXXXXX', 'notificationOptIn': True, 'termsOptIn': True, 'emailVerified': False, 'name': {'first': 'XXXXXXXXX', 'last': 'XXXXXXXXX'}, 'phone': None, 'language': 'en_US', 'lastUpdated': '2023-10-12T00:21:12.725773Z', 'voiceEnabledSpaId': None, 'sutroNotifications': True, 'atEaseEnabled': None}
2023-10-19 09:05:45.668 DEBUG (MainThread) [smarttub.api] get_account successful: {'id': 'XXXXXXXXXX ', 'email': 'XXXXXXXXXXXXXXXXX', 'notificationOptIn': True, 'termsOptIn': True, 'emailVerified': False, 'name': {'first': 'XXXXXXXXX', 'last': 'XXXXXXXXX'}, 'phone': None, 'language': 'en_US', 'lastUpdated': '2023-10-12T00:21:12.725773Z', 'voiceEnabledSpaId': None, 'sutroNotifications': True, 'atEaseEnabled': None}
2023-10-19 09:05:45.879 DEBUG (MainThread) [smarttub.api] GET spas?ownerId=XXXXXXXXXX successful: {'content': [{'id': '100952654', 'dealerId': None, 'ownerId': 'XXXXXXXXXX ', 'name': None, 'dealer': None, 'owner': {'id': 'XXXXXXXXXX ', 'email': 'XXXXXXXXXXXXXXXXX', 'notificationOptIn': True, 'termsOptIn': True, 'emailVerified': False, 'name': {'first': 'XXXXXXXXX', 'last': 'XXXXXXXXX'}, 'phone': None, 'language': 'en_US', 'lastUpdated': '2023-10-12T00:21:12.725773Z', 'voiceEnabledSpaId': None, 'sutroNotifications': True, 'atEaseEnabled': None}, 'deviceId': 'e00fce68817a0de421b6d257', 'device': {'id': 'e00fce68817a0de421b6d257', 'barcode': 'P007AD228LM7KH2'}, 'selfTest': {'status': 'FAIL', 'current': {'heaterAndCirculationPump': 20.6, 'jets': [{'spaId': '100952654', 'pumpId': 'P1', 'current': 9.1}, {'spaId': '100952654', 'pumpId': 'P2', 'current': 8.7}], 'blower': -99.9, 'circulationPump': None, 'ozone': None, 'ultraviolet': None}, 'frequency': 'DAILY', 'startTime': None, 'lastTestTime': '2014-01-01T12:07:00Z'}, 'brand': 'Jacuzzi', 'series': 'J-200', 'modelNumber': 'Z6120AKDM', 'model': 'J-280', 'stereo': False, 'tubColor': 12, 'cabinetColor': 'A', 'equipmentOption': '0', 'revision': 'K', 'ecomode': False, 'volume': 460, 'pairedAt': '2023-10-12T00:23:21.535777Z', 'subscriptionExpiredAt': None, 'subscriptions': None, 'deviceOptIn': False, 'deviceOnline': False, 'powerResetRequired': False, 'voltage': 240, 'warrantyDate': '2023-09-27', 'createdAt': '2023-04-14T20:13:41.267', 'createdSource': 'MANUFACTURING', 'adapter': 'OFF', 'productIdOrSlug': 'smarttub-ble-na-14893', 'us3G': False, '_b402Upgrade': False, 'sutro': None, 'location': None, 'signal': None, 'coupon': [], 'heaterWatts': 5405, 'coolingRate': 4.88e-07, 'avgAmbientTemp': None, 'ir': False, 'appSettings': None, 'current': {'value': 3.1, 'min': 3.0, 'max': 3.1, 'average': 3.1, 'kwh': 0.411}, 'water': {'oxidationReductionPotential': None, 'ph': None, 'temperature': 38.9, 'turbidity': None, 'temperatureLastUpdated': '2023-10-19T15:00:48.176Z'}, 'lastUpdated': '2023-10-19T15:06:35.322Z'}], 'pageable': {'sort': {'sorted': True, 'unsorted': False, 'empty': False}, 'offset': 0, 'pageSize': 10, 'pageNumber': 0, 'unpaged': False, 'paged': True}, 'last': True, 'totalPages': 1, 'totalElements': 1, 'size': 10, 'number': 0, 'sort': {'sorted': True, 'unsorted': False, 'empty': False}, 'first': True, 'numberOfElements': 1, 'empty': False}
2023-10-19 09:05:46.042 DEBUG (MainThread) [smarttub.api] GET spas/100952654 successful: {'id': '100952654', 'dealerId': None, 'ownerId': 'XXXXXXXXXX ', 'name': None, 'dealer': None, 'owner': {'id': 'XXXXXXXXXX ', 'email': 'XXXXXXXXXXXXXXXXX', 'notificationOptIn': True, 'termsOptIn': True, 'emailVerified': False, 'name': {'first': 'XXXXXXXXX', 'last': 'XXXXXXXXX'}, 'phone': None, 'language': 'en_US', 'lastUpdated': '2023-10-12T00:21:12.725773Z', 'voiceEnabledSpaId': None, 'sutroNotifications': True, 'atEaseEnabled': None}, 'deviceId': 'e00fce68817a0de421b6d257', 'device': {'id': 'e00fce68817a0de421b6d257', 'barcode': 'P007AD228LM7KH2'}, 'selfTest': {'status': 'FAIL', 'current': {'heaterAndCirculationPump': 20.6, 'jets': [{'spaId': '100952654', 'pumpId': 'P1', 'current': 9.1}, {'spaId': '100952654', 'pumpId': 'P2', 'current': 8.7}], 'blower': -99.9, 'circulationPump': None, 'ozone': None, 'ultraviolet': None}, 'frequency': 'DAILY', 'startTime': None, 'lastTestTime': '2014-01-01T12:07:00Z'}, 'brand': 'Jacuzzi', 'series': 'J-200', 'modelNumber': 'Z6120AKDM', 'model': 'J-280', 'stereo': False, 'tubColor': 12, 'cabinetColor': 'A', 'equipmentOption': '0', 'revision': 'K', 'ecomode': False, 'volume': 460, 'pairedAt': '2023-10-12T00:23:21.535777Z', 'subscriptionExpiredAt': None, 'subscriptions': None, 'deviceOptIn': True, 'deviceOnline': True, 'powerResetRequired': False, 'voltage': 240, 'warrantyDate': '2023-09-27', 'createdAt': '2023-04-14T20:13:41.267', 'createdSource': 'MANUFACTURING', 'adapter': 'OFF', 'productIdOrSlug': 'smarttub-ble-na-14893', 'us3G': False, '_b402Upgrade': False, 'sutro': None, 'location': None, 'signal': None, 'coupon': [], 'heaterWatts': 5405, 'coolingRate': 4.88e-07, 'avgAmbientTemp': None, 'ir': False, 'appSettings': None, 'current': {'value': 3.1, 'min': 3.0, 'max': 3.1, 'average': 3.1, 'kwh': 0.411}, 'water': {'oxidationReductionPotential': None, 'ph': None, 'temperature': 38.9, 'turbidity': None, 'temperatureLastUpdated': '2023-10-19T15:00:48.176Z'}, 'lastUpdated': '2023-10-19T15:06:35.322Z'}
2023-10-19 09:05:46.323 DEBUG (MainThread) [smarttub.api] GET spas/100952654/errors successful: {'content': [], 'pageable': {'sort': {'sorted': True, 'unsorted': False, 'empty': False}, 'offset': 0, 'pageSize': 10, 'pageNumber': 0, 'paged': True, 'unpaged': False}, 'totalPages': 0, 'totalElements': 0, 'last': True, 'size': 10, 'number': 0, 'sort': {'sorted': True, 'unsorted': False, 'empty': False}, 'first': True, 'numberOfElements': 0, 'empty': True}
2023-10-19 09:05:46.324 DEBUG (MainThread) [smarttub.api] GET spas/100952654/reminders successful: {'reminders': [{'id': 'FILTER01', 'name': 'Filter', 'state': 'INACTIVE', 'remainingDuration': 0, 'snoozed': False, 'lastUpdated': None, 'startDate': None, 'durationDays': None, 'activeTimestamp': None}, {'id': 'FILTER02', 'name': 'Filter', 'state': 'INACTIVE', 'remainingDuration': 0, 'snoozed': False, 'lastUpdated': None, 'startDate': None, 'durationDays': None, 'activeTimestamp': None}, {'id': 'CLEARRAY', 'name': 'ClearRay', 'state': 'INACTIVE', 'remainingDuration': 0, 'snoozed': False, 'lastUpdated': None, 'startDate': None, 'durationDays': None, 'activeTimestamp': None}, {'id': 'WATER', 'name': 'Refresh Water', 'state': 'INACTIVE', 'remainingDuration': 0, 'snoozed': False, 'lastUpdated': None, 'startDate': None, 'durationDays': None, 'activeTimestamp': None}], 'filters': [{'id': 'FILTER01', 'name': 'Filter', 'state': 'INACTIVE', 'remainingDuration': 0, 'snoozed': False, 'lastUpdated': None, 'startDate': None, 'durationDays': None, 'activeTimestamp': None}, {'id': 'FILTER02', 'name': 'Filter', 'state': 'INACTIVE', 'remainingDuration': 0, 'snoozed': False, 'lastUpdated': None, 'startDate': None, 'durationDays': None, 'activeTimestamp': None}, {'id': 'CLEARRAY', 'name': 'ClearRay', 'state': 'INACTIVE', 'remainingDuration': 0, 'snoozed': False, 'lastUpdated': None, 'startDate': None, 'durationDays': None, 'activeTimestamp': None}, {'id': 'WATER', 'name': 'Refresh Water', 'state': 'INACTIVE', 'remainingDuration': 0, 'snoozed': False, 'lastUpdated': None, 'startDate': None, 'durationDays': None, 'activeTimestamp': None}]}
2023-10-19 09:05:46.326 DEBUG (MainThread) [smarttub.api] GET spas/100952654/fullStatus successful: {'ambientTemperature': None, 'blowoutCycle': None, 'cleanupCycle': 'INACTIVE', 'date': None, 'demoMode': 'DISABLED', 'dipSwitches': 2, 'displayTemperatureFormat': 'FAHRENHEIT', 'errorCode': 0, 'error': {'code': 0, 'title': 'All Clear', 'description': None}, 'flowSwitch': None, 'heater': 'OFF', 'heatMode': 'READY', 'highTemperatureLimit': None, 'lastUpdated': '2023-10-19T15:06:35.322Z', 'state': 'INIT', 'ozone': 'ON', 'setTemperature': 38.9, 'time': '00:06:00', 'timeFormat': 'HOURS_12', 'timezone': None, 'uv': 'OFF', 'uvOnDemand': 'OFF', 'current': {'value': 3.1, 'min': 3.0, 'max': 3.1, 'average': 3.1, 'kwh': 0.411}, 'primaryFiltration': {'mode': 'NORMAL', 'status': 'INACTIVE', 'startHour': 20, 'duration': 4, 'cycle': 0, 'startMinute': 0, 'durationMinute': 0, 'lastUpdated': '2023-10-19T07:06:26.871Z'}, 'secondaryFiltration': {'mode': 'AWAY', 'status': 'ACTIVE', 'enabled': True, 'startHour': 8, 'startMinute': 0, 'durationHour': 4, 'durationMinute': 0, 'lastUpdated': '2023-10-19T14:59:47.344Z'}, 'water': {'oxidationReductionPotential': None, 'ph': None, 'temperature': 38.9, 'turbidity': None, 'temperatureLastUpdated': '2023-10-19T15:00:48.176Z'}, 'versions': {'balboa': '1.09', 'controller': '62.00', 'jacuzziLink': '81'}, 'locks': {'temperature': 'UNLOCKED', 'spa': 'UNLOCKED', 'access': 'UNLOCKED', 'maintenance': 'UNLOCKED'}, 'location': {'latitude': 47.7516708, 'longitude': -121.9901199, 'accuracy': 3010.0}, 'fieldsLastUpdated': {'heatMode': '2023-10-19T07:06:26.871Z', 'setTemperature': '2023-10-19T07:06:26.871Z', 'uv': '2023-10-19T07:06:26.871Z', 'uvOnDemand': '2023-10-19T07:06:26.871Z', 'online': None, 'errEvent': '2023-10-12T00:26:08.512Z', 'locEvent': '2023-10-17T01:48:20.524Z', 'rpstEvent': '2023-10-19T15:00:48.021Z', 'spstEvent': '2023-10-19T15:06:35.165Z', 'cfstEvent': '2023-10-19T07:06:24.156Z', 'sp2stEvent': '2023-10-19T07:06:25.676Z', 'wcstEvent': None}, 'watercare': None, 'online': None, 'pumps': [{'id': 'P2', 'type': 'JET', 'state': 'OFF', 'speed': 'ONE_SPEED', 'current': None}, {'id': 'P1', 'type': 'JET', 'state': 'LOW', 'speed': 'TWO_SPEED', 'current': None}], 'lights': [{'zone': 1, 'mode': 'ON', 'cycleSpeed': 0, 'color': {'red': 0, 'blue': 0, 'green': 0, 'white': 0}, 'intensity': 0, 'irt': None, 'exterior': False}], 'sensors': [], 'lowRangeLowTemp': 65, 'lowRangeHighTemp': 99, 'highRangeLowTemp': 80, 'highRangeHighTemp': 104, 'tempRange': 'HIGH', 'heater1Present': 'PRESENT', 'heater2Present': 'NOT_PRESENT', 'ozoneSystemPresent': 'NOT_PRESENT', 'primingMode': 'INACTIVE', 'heater2On': 'OFF', 'heatPumpStatus': 'NOT_PRESENT', 'heatPumpMode': 'DISABLED', 'heatPumpEfficiency': 'AUTO_SMART', 'electricHeaterMode': 'M7', 'czStatus': 'NOT_PRESENT', 'chromazon3Present': 'OFF', 'chromazon3Zone1': 'FULL_CONTROL', 'chromazon3Zone2': 'FULL_CONTROL', 'chromazon3Zone3': 'FULL_CONTROL', 'heatCanWait': 4, 'heatVacation': False, 'signal': {'strength': 12, 'quality': 6, 'signalAt': None, 'country': 'US', 'updateAt': '2023-10-19T11:45:54.049Z'}, 'errors': [], 'timeSet': None}
2023-10-19 09:05:46.327 ERROR (MainThread) [smarttub.api] Failed to parse fullStatus response: {'ambientTemperature': None, 'blowoutCycle': None, 'cleanupCycle': 'INACTIVE', 'date': None, 'demoMode': 'DISABLED', 'dipSwitches': 2, 'displayTemperatureFormat': 'FAHRENHEIT', 'errorCode': 0, 'error': {'code': 0, 'title': 'All Clear', 'description': None}, 'flowSwitch': None, 'heater': 'OFF', 'heatMode': 'READY', 'highTemperatureLimit': None, 'lastUpdated': '2023-10-19T15:06:35.322Z', 'state': 'INIT', 'ozone': 'ON', 'setTemperature': 38.9, 'time': '00:06:00', 'timeFormat': 'HOURS_12', 'timezone': None, 'uv': 'OFF', 'uvOnDemand': 'OFF', 'current': {'value': 3.1, 'min': 3.0, 'max': 3.1, 'average': 3.1, 'kwh': 0.411}, 'primaryFiltration': {'mode': 'NORMAL', 'status': 'INACTIVE', 'startHour': 20, 'duration': 4, 'cycle': 0, 'startMinute': 0, 'durationMinute': 0, 'lastUpdated': '2023-10-19T07:06:26.871Z'}, 'secondaryFiltration': {'mode': 'AWAY', 'status': 'ACTIVE', 'enabled': True, 'startHour': 8, 'startMinute': 0, 'durationHour': 4, 'durationMinute': 0, 'lastUpdated': '2023-10-19T14:59:47.344Z'}, 'water': {'oxidationReductionPotential': None, 'ph': None, 'temperature': 38.9, 'turbidity': None, 'temperatureLastUpdated': '2023-10-19T15:00:48.176Z'}, 'versions': {'balboa': '1.09', 'controller': '62.00', 'jacuzziLink': '81'}, 'locks': {'temperature': 'UNLOCKED', 'spa': 'UNLOCKED', 'access': 'UNLOCKED', 'maintenance': 'UNLOCKED'}, 'location': {'latitude': 47.7516708, 'longitude': -121.9901199, 'accuracy': 3010.0}, 'fieldsLastUpdated': {'heatMode': '2023-10-19T07:06:26.871Z', 'setTemperature': '2023-10-19T07:06:26.871Z', 'uv': '2023-10-19T07:06:26.871Z', 'uvOnDemand': '2023-10-19T07:06:26.871Z', 'online': None, 'errEvent': '2023-10-12T00:26:08.512Z', 'locEvent': '2023-10-17T01:48:20.524Z', 'rpstEvent': '2023-10-19T15:00:48.021Z', 'spstEvent': '2023-10-19T15:06:35.165Z', 'cfstEvent': '2023-10-19T07:06:24.156Z', 'sp2stEvent': '2023-10-19T07:06:25.676Z', 'wcstEvent': None}, 'watercare': None, 'online': None, 'pumps': [{'id': 'P2', 'type': 'JET', 'state': 'OFF', 'speed': 'ONE_SPEED', 'current': None}, {'id': 'P1', 'type': 'JET', 'state': 'LOW', 'speed': 'TWO_SPEED', 'current': None}], 'lights': [{'zone': 1, 'mode': 'ON', 'cycleSpeed': 0, 'color': {'red': 0, 'blue': 0, 'green': 0, 'white': 0}, 'intensity': 0, 'irt': None, 'exterior': False}], 'sensors': [], 'lowRangeLowTemp': 65, 'lowRangeHighTemp': 99, 'highRangeLowTemp': 80, 'highRangeHighTemp': 104, 'tempRange': 'HIGH', 'heater1Present': 'PRESENT', 'heater2Present': 'NOT_PRESENT', 'ozoneSystemPresent': 'NOT_PRESENT', 'primingMode': 'INACTIVE', 'heater2On': 'OFF', 'heatPumpStatus': 'NOT_PRESENT', 'heatPumpMode': 'DISABLED', 'heatPumpEfficiency': 'AUTO_SMART', 'electricHeaterMode': 'M7', 'czStatus': 'NOT_PRESENT', 'chromazon3Present': 'OFF', 'chromazon3Zone1': 'FULL_CONTROL', 'chromazon3Zone2': 'FULL_CONTROL', 'chromazon3Zone3': 'FULL_CONTROL', 'heatCanWait': 4, 'heatVacation': False, 'signal': {'strength': 12, 'quality': 6, 'signalAt': None, 'country': 'US', 'updateAt': '2023-10-19T11:45:54.049Z'}, 'errors': [], 'timeSet': None}
2023-10-19 09:05:46.363 ERROR (MainThread) [homeassistant.components.smarttub.controller] Unexpected error fetching smarttub data: None
Traceback (most recent call last):
File "/usr/src/homeassistant/homeassistant/helpers/update_coordinator.py", line 290, in _async_refresh
self.data = await self._async_update_data()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/src/homeassistant/homeassistant/helpers/update_coordinator.py", line 246, in _async_update_data
return await self.update_method()
^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/src/homeassistant/homeassistant/components/smarttub/controller.py", line 89, in async_update_data
data[spa.id] = await self._get_spa_data(spa)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/src/homeassistant/homeassistant/components/smarttub/controller.py", line 96, in _get_spa_data
full_status, reminders, errors = await asyncio.gather(
^^^^^^^^^^^^^^^^^^^^^
File "/usr/local/lib/python3.11/site-packages/smarttub/api.py", line 215, in get_status_full
return SpaStateFull(self, full_status)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/local/lib/python3.11/site-packages/smarttub/api.py", line 352, in __init__
super().__init__(spa, **state)
File "/usr/local/lib/python3.11/site-packages/smarttub/api.py", line 280, in __init__
self._prop("blowoutCycle", constructor=lambda x: self.CycleStatus[x])
File "/usr/local/lib/python3.11/site-packages/smarttub/api.py", line 341, in _prop
self, instance_variable_name, constructor(self.properties[json_key])
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/local/lib/python3.11/site-packages/smarttub/api.py", line 280, in <lambda>
self._prop("blowoutCycle", constructor=lambda x: self.CycleStatus[x])
~~~~~~~~~~~~~~~~^^^
File "/usr/local/lib/python3.11/enum.py", line 790, in __getitem__
return cls._member_map_[name]
~~~~~~~~~~~~~~~~^^^^^^
KeyError: None
2023-10-19 09:05:46.384 DEBUG (MainThread) [homeassistant.components.smarttub.controller] Finished fetching smarttub data in 0.311 seconds (success: False)
2023-10-19 09:05:46.594 ERROR (MainThread) [homeassistant.components.binary_sensor] Error while setting up smarttub platform for binary_sensor
Traceback (most recent call last):
File "/usr/src/homeassistant/homeassistant/helpers/entity_platform.py", line 359, in _async_setup_platform
await asyncio.shield(task)
File "/usr/src/homeassistant/homeassistant/components/smarttub/binary_sensor.py", line 56, in async_setup_entry
for reminder in controller.coordinator.data[spa.id][ATTR_REMINDERS].values()
~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
TypeError: 'NoneType' object is not subscriptable
2023-10-19 09:05:46.604 ERROR (MainThread) [homeassistant.components.light] Error while setting up smarttub platform for light
Traceback (most recent call last):
File "/usr/src/homeassistant/homeassistant/helpers/entity_platform.py", line 359, in _async_setup_platform
await asyncio.shield(task)
File "/usr/src/homeassistant/homeassistant/components/smarttub/light.py", line 36, in async_setup_entry
entities = [
^
File "/usr/src/homeassistant/homeassistant/components/smarttub/light.py", line 39, in <listcomp>
for light in controller.coordinator.data[spa.id][ATTR_LIGHTS].values()
~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
TypeError: 'NoneType' object is not subscriptable
2023-10-19 09:05:46.624 ERROR (MainThread) [homeassistant.components.switch] Error while setting up smarttub platform for switch
Traceback (most recent call last):
File "/usr/src/homeassistant/homeassistant/helpers/entity_platform.py", line 359, in _async_setup_platform
await asyncio.shield(task)
File "/usr/src/homeassistant/homeassistant/components/smarttub/switch.py", line 24, in async_setup_entry
entities = [
^
File "/usr/src/homeassistant/homeassistant/components/smarttub/switch.py", line 27, in <listcomp>
for pump in controller.coordinator.data[spa.id][ATTR_PUMPS].values()
~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
TypeError: 'NoneType' object is not subscriptable`

### Example YAML snippet

_No response_

### Anything in the logs that might be useful for us?

```txt
`2023-10-19 09:05:45.434 DEBUG (MainThread) [smarttub.api] login successful, username=XXXXXXXXXXXXXXXXX
2023-10-19 09:05:45.668 DEBUG (MainThread) [smarttub.api] GET accounts/XXXXXXXXXX successful: {'id': 'XXXXXXXXXX ', 'email': 'XXXXXXXXXXXXXXXXX', 'notificationOptIn': True, 'termsOptIn': True, 'emailVerified': False, 'name': {'first': 'XXXXXXXXX', 'last': 'XXXXXXXXX'}, 'phone': None, 'language': 'en_US', 'lastUpdated': '2023-10-12T00:21:12.725773Z', 'voiceEnabledSpaId': None, 'sutroNotifications': True, 'atEaseEnabled': None}
2023-10-19 09:05:45.668 DEBUG (MainThread) [smarttub.api] get_account successful: {'id': 'XXXXXXXXXX ', 'email': 'XXXXXXXXXXXXXXXXX', 'notificationOptIn': True, 'termsOptIn': True, 'emailVerified': False, 'name': {'first': 'XXXXXXXXX', 'last': 'XXXXXXXXX'}, 'phone': None, 'language': 'en_US', 'lastUpdated': '2023-10-12T00:21:12.725773Z', 'voiceEnabledSpaId': None, 'sutroNotifications': True, 'atEaseEnabled': None}
2023-10-19 09:05:45.879 DEBUG (MainThread) [smarttub.api] GET spas?ownerId=XXXXXXXXXX successful: {'content': [{'id': '100952654', 'dealerId': None, 'ownerId': 'XXXXXXXXXX ', 'name': None, 'dealer': None, 'owner': {'id': 'XXXXXXXXXX ', 'email': 'XXXXXXXXXXXXXXXXX', 'notificationOptIn': True, 'termsOptIn': True, 'emailVerified': False, 'name': {'first': 'XXXXXXXXX', 'last': 'XXXXXXXXX'}, 'phone': None, 'language': 'en_US', 'lastUpdated': '2023-10-12T00:21:12.725773Z', 'voiceEnabledSpaId': None, 'sutroNotifications': True, 'atEaseEnabled': None}, 'deviceId': 'e00fce68817a0de421b6d257', 'device': {'id': 'e00fce68817a0de421b6d257', 'barcode': 'P007AD228LM7KH2'}, 'selfTest': {'status': 'FAIL', 'current': {'heaterAndCirculationPump': 20.6, 'jets': [{'spaId': '100952654', 'pumpId': 'P1', 'current': 9.1}, {'spaId': '100952654', 'pumpId': 'P2', 'current': 8.7}], 'blower': -99.9, 'circulationPump': None, 'ozone': None, 'ultraviolet': None}, 'frequency': 'DAILY', 'startTime': None, 'lastTestTime': '2014-01-01T12:07:00Z'}, 'brand': 'Jacuzzi', 'series': 'J-200', 'modelNumber': 'Z6120AKDM', 'model': 'J-280', 'stereo': False, 'tubColor': 12, 'cabinetColor': 'A', 'equipmentOption': '0', 'revision': 'K', 'ecomode': False, 'volume': 460, 'pairedAt': '2023-10-12T00:23:21.535777Z', 'subscriptionExpiredAt': None, 'subscriptions': None, 'deviceOptIn': False, 'deviceOnline': False, 'powerResetRequired': False, 'voltage': 240, 'warrantyDate': '2023-09-27', 'createdAt': '2023-04-14T20:13:41.267', 'createdSource': 'MANUFACTURING', 'adapter': 'OFF', 'productIdOrSlug': 'smarttub-ble-na-14893', 'us3G': False, '_b402Upgrade': False, 'sutro': None, 'location': None, 'signal': None, 'coupon': [], 'heaterWatts': 5405, 'coolingRate': 4.88e-07, 'avgAmbientTemp': None, 'ir': False, 'appSettings': None, 'current': {'value': 3.1, 'min': 3.0, 'max': 3.1, 'average': 3.1, 'kwh': 0.411}, 'water': {'oxidationReductionPotential': None, 'ph': None, 'temperature': 38.9, 'turbidity': None, 'temperatureLastUpdated': '2023-10-19T15:00:48.176Z'}, 'lastUpdated': '2023-10-19T15:06:35.322Z'}], 'pageable': {'sort': {'sorted': True, 'unsorted': False, 'empty': False}, 'offset': 0, 'pageSize': 10, 'pageNumber': 0, 'unpaged': False, 'paged': True}, 'last': True, 'totalPages': 1, 'totalElements': 1, 'size': 10, 'number': 0, 'sort': {'sorted': True, 'unsorted': False, 'empty': False}, 'first': True, 'numberOfElements': 1, 'empty': False}
2023-10-19 09:05:46.042 DEBUG (MainThread) [smarttub.api] GET spas/100952654 successful: {'id': '100952654', 'dealerId': None, 'ownerId': 'XXXXXXXXXX ', 'name': None, 'dealer': None, 'owner': {'id': 'XXXXXXXXXX ', 'email': 'XXXXXXXXXXXXXXXXX', 'notificationOptIn': True, 'termsOptIn': True, 'emailVerified': False, 'name': {'first': 'XXXXXXXXX', 'last': 'XXXXXXXXX'}, 'phone': None, 'language': 'en_US', 'lastUpdated': '2023-10-12T00:21:12.725773Z', 'voiceEnabledSpaId': None, 'sutroNotifications': True, 'atEaseEnabled': None}, 'deviceId': 'e00fce68817a0de421b6d257', 'device': {'id': 'e00fce68817a0de421b6d257', 'barcode': 'P007AD228LM7KH2'}, 'selfTest': {'status': 'FAIL', 'current': {'heaterAndCirculationPump': 20.6, 'jets': [{'spaId': '100952654', 'pumpId': 'P1', 'current': 9.1}, {'spaId': '100952654', 'pumpId': 'P2', 'current': 8.7}], 'blower': -99.9, 'circulationPump': None, 'ozone': None, 'ultraviolet': None}, 'frequency': 'DAILY', 'startTime': None, 'lastTestTime': '2014-01-01T12:07:00Z'}, 'brand': 'Jacuzzi', 'series': 'J-200', 'modelNumber': 'Z6120AKDM', 'model': 'J-280', 'stereo': False, 'tubColor': 12, 'cabinetColor': 'A', 'equipmentOption': '0', 'revision': 'K', 'ecomode': False, 'volume': 460, 'pairedAt': '2023-10-12T00:23:21.535777Z', 'subscriptionExpiredAt': None, 'subscriptions': None, 'deviceOptIn': True, 'deviceOnline': True, 'powerResetRequired': False, 'voltage': 240, 'warrantyDate': '2023-09-27', 'createdAt': '2023-04-14T20:13:41.267', 'createdSource': 'MANUFACTURING', 'adapter': 'OFF', 'productIdOrSlug': 'smarttub-ble-na-14893', 'us3G': False, '_b402Upgrade': False, 'sutro': None, 'location': None, 'signal': None, 'coupon': [], 'heaterWatts': 5405, 'coolingRate': 4.88e-07, 'avgAmbientTemp': None, 'ir': False, 'appSettings': None, 'current': {'value': 3.1, 'min': 3.0, 'max': 3.1, 'average': 3.1, 'kwh': 0.411}, 'water': {'oxidationReductionPotential': None, 'ph': None, 'temperature': 38.9, 'turbidity': None, 'temperatureLastUpdated': '2023-10-19T15:00:48.176Z'}, 'lastUpdated': '2023-10-19T15:06:35.322Z'}
2023-10-19 09:05:46.323 DEBUG (MainThread) [smarttub.api] GET spas/100952654/errors successful: {'content': [], 'pageable': {'sort': {'sorted': True, 'unsorted': False, 'empty': False}, 'offset': 0, 'pageSize': 10, 'pageNumber': 0, 'paged': True, 'unpaged': False}, 'totalPages': 0, 'totalElements': 0, 'last': True, 'size': 10, 'number': 0, 'sort': {'sorted': True, 'unsorted': False, 'empty': False}, 'first': True, 'numberOfElements': 0, 'empty': True}
2023-10-19 09:05:46.324 DEBUG (MainThread) [smarttub.api] GET spas/100952654/reminders successful: {'reminders': [{'id': 'FILTER01', 'name': 'Filter', 'state': 'INACTIVE', 'remainingDuration': 0, 'snoozed': False, 'lastUpdated': None, 'startDate': None, 'durationDays': None, 'activeTimestamp': None}, {'id': 'FILTER02', 'name': 'Filter', 'state': 'INACTIVE', 'remainingDuration': 0, 'snoozed': False, 'lastUpdated': None, 'startDate': None, 'durationDays': None, 'activeTimestamp': None}, {'id': 'CLEARRAY', 'name': 'ClearRay', 'state': 'INACTIVE', 'remainingDuration': 0, 'snoozed': False, 'lastUpdated': None, 'startDate': None, 'durationDays': None, 'activeTimestamp': None}, {'id': 'WATER', 'name': 'Refresh Water', 'state': 'INACTIVE', 'remainingDuration': 0, 'snoozed': False, 'lastUpdated': None, 'startDate': None, 'durationDays': None, 'activeTimestamp': None}], 'filters': [{'id': 'FILTER01', 'name': 'Filter', 'state': 'INACTIVE', 'remainingDuration': 0, 'snoozed': False, 'lastUpdated': None, 'startDate': None, 'durationDays': None, 'activeTimestamp': None}, {'id': 'FILTER02', 'name': 'Filter', 'state': 'INACTIVE', 'remainingDuration': 0, 'snoozed': False, 'lastUpdated': None, 'startDate': None, 'durationDays': None, 'activeTimestamp': None}, {'id': 'CLEARRAY', 'name': 'ClearRay', 'state': 'INACTIVE', 'remainingDuration': 0, 'snoozed': False, 'lastUpdated': None, 'startDate': None, 'durationDays': None, 'activeTimestamp': None}, {'id': 'WATER', 'name': 'Refresh Water', 'state': 'INACTIVE', 'remainingDuration': 0, 'snoozed': False, 'lastUpdated': None, 'startDate': None, 'durationDays': None, 'activeTimestamp': None}]}
2023-10-19 09:05:46.326 DEBUG (MainThread) [smarttub.api] GET spas/100952654/fullStatus successful: {'ambientTemperature': None, 'blowoutCycle': None, 'cleanupCycle': 'INACTIVE', 'date': None, 'demoMode': 'DISABLED', 'dipSwitches': 2, 'displayTemperatureFormat': 'FAHRENHEIT', 'errorCode': 0, 'error': {'code': 0, 'title': 'All Clear', 'description': None}, 'flowSwitch': None, 'heater': 'OFF', 'heatMode': 'READY', 'highTemperatureLimit': None, 'lastUpdated': '2023-10-19T15:06:35.322Z', 'state': 'INIT', 'ozone': 'ON', 'setTemperature': 38.9, 'time': '00:06:00', 'timeFormat': 'HOURS_12', 'timezone': None, 'uv': 'OFF', 'uvOnDemand': 'OFF', 'current': {'value': 3.1, 'min': 3.0, 'max': 3.1, 'average': 3.1, 'kwh': 0.411}, 'primaryFiltration': {'mode': 'NORMAL', 'status': 'INACTIVE', 'startHour': 20, 'duration': 4, 'cycle': 0, 'startMinute': 0, 'durationMinute': 0, 'lastUpdated': '2023-10-19T07:06:26.871Z'}, 'secondaryFiltration': {'mode': 'AWAY', 'status': 'ACTIVE', 'enabled': True, 'startHour': 8, 'startMinute': 0, 'durationHour': 4, 'durationMinute': 0, 'lastUpdated': '2023-10-19T14:59:47.344Z'}, 'water': {'oxidationReductionPotential': None, 'ph': None, 'temperature': 38.9, 'turbidity': None, 'temperatureLastUpdated': '2023-10-19T15:00:48.176Z'}, 'versions': {'balboa': '1.09', 'controller': '62.00', 'jacuzziLink': '81'}, 'locks': {'temperature': 'UNLOCKED', 'spa': 'UNLOCKED', 'access': 'UNLOCKED', 'maintenance': 'UNLOCKED'}, 'location': {'latitude': 47.7516708, 'longitude': -121.9901199, 'accuracy': 3010.0}, 'fieldsLastUpdated': {'heatMode': '2023-10-19T07:06:26.871Z', 'setTemperature': '2023-10-19T07:06:26.871Z', 'uv': '2023-10-19T07:06:26.871Z', 'uvOnDemand': '2023-10-19T07:06:26.871Z', 'online': None, 'errEvent': '2023-10-12T00:26:08.512Z', 'locEvent': '2023-10-17T01:48:20.524Z', 'rpstEvent': '2023-10-19T15:00:48.021Z', 'spstEvent': '2023-10-19T15:06:35.165Z', 'cfstEvent': '2023-10-19T07:06:24.156Z', 'sp2stEvent': '2023-10-19T07:06:25.676Z', 'wcstEvent': None}, 'watercare': None, 'online': None, 'pumps': [{'id': 'P2', 'type': 'JET', 'state': 'OFF', 'speed': 'ONE_SPEED', 'current': None}, {'id': 'P1', 'type': 'JET', 'state': 'LOW', 'speed': 'TWO_SPEED', 'current': None}], 'lights': [{'zone': 1, 'mode': 'ON', 'cycleSpeed': 0, 'color': {'red': 0, 'blue': 0, 'green': 0, 'white': 0}, 'intensity': 0, 'irt': None, 'exterior': False}], 'sensors': [], 'lowRangeLowTemp': 65, 'lowRangeHighTemp': 99, 'highRangeLowTemp': 80, 'highRangeHighTemp': 104, 'tempRange': 'HIGH', 'heater1Present': 'PRESENT', 'heater2Present': 'NOT_PRESENT', 'ozoneSystemPresent': 'NOT_PRESENT', 'primingMode': 'INACTIVE', 'heater2On': 'OFF', 'heatPumpStatus': 'NOT_PRESENT', 'heatPumpMode': 'DISABLED', 'heatPumpEfficiency': 'AUTO_SMART', 'electricHeaterMode': 'M7', 'czStatus': 'NOT_PRESENT', 'chromazon3Present': 'OFF', 'chromazon3Zone1': 'FULL_CONTROL', 'chromazon3Zone2': 'FULL_CONTROL', 'chromazon3Zone3': 'FULL_CONTROL', 'heatCanWait': 4, 'heatVacation': False, 'signal': {'strength': 12, 'quality': 6, 'signalAt': None, 'country': 'US', 'updateAt': '2023-10-19T11:45:54.049Z'}, 'errors': [], 'timeSet': None}
2023-10-19 09:05:46.327 ERROR (MainThread) [smarttub.api] Failed to parse fullStatus response: {'ambientTemperature': None, 'blowoutCycle': None, 'cleanupCycle': 'INACTIVE', 'date': None, 'demoMode': 'DISABLED', 'dipSwitches': 2, 'displayTemperatureFormat': 'FAHRENHEIT', 'errorCode': 0, 'error': {'code': 0, 'title': 'All Clear', 'description': None}, 'flowSwitch': None, 'heater': 'OFF', 'heatMode': 'READY', 'highTemperatureLimit': None, 'lastUpdated': '2023-10-19T15:06:35.322Z', 'state': 'INIT', 'ozone': 'ON', 'setTemperature': 38.9, 'time': '00:06:00', 'timeFormat': 'HOURS_12', 'timezone': None, 'uv': 'OFF', 'uvOnDemand': 'OFF', 'current': {'value': 3.1, 'min': 3.0, 'max': 3.1, 'average': 3.1, 'kwh': 0.411}, 'primaryFiltration': {'mode': 'NORMAL', 'status': 'INACTIVE', 'startHour': 20, 'duration': 4, 'cycle': 0, 'startMinute': 0, 'durationMinute': 0, 'lastUpdated': '2023-10-19T07:06:26.871Z'}, 'secondaryFiltration': {'mode': 'AWAY', 'status': 'ACTIVE', 'enabled': True, 'startHour': 8, 'startMinute': 0, 'durationHour': 4, 'durationMinute': 0, 'lastUpdated': '2023-10-19T14:59:47.344Z'}, 'water': {'oxidationReductionPotential': None, 'ph': None, 'temperature': 38.9, 'turbidity': None, 'temperatureLastUpdated': '2023-10-19T15:00:48.176Z'}, 'versions': {'balboa': '1.09', 'controller': '62.00', 'jacuzziLink': '81'}, 'locks': {'temperature': 'UNLOCKED', 'spa': 'UNLOCKED', 'access': 'UNLOCKED', 'maintenance': 'UNLOCKED'}, 'location': {'latitude': 47.7516708, 'longitude': -121.9901199, 'accuracy': 3010.0}, 'fieldsLastUpdated': {'heatMode': '2023-10-19T07:06:26.871Z', 'setTemperature': '2023-10-19T07:06:26.871Z', 'uv': '2023-10-19T07:06:26.871Z', 'uvOnDemand': '2023-10-19T07:06:26.871Z', 'online': None, 'errEvent': '2023-10-12T00:26:08.512Z', 'locEvent': '2023-10-17T01:48:20.524Z', 'rpstEvent': '2023-10-19T15:00:48.021Z', 'spstEvent': '2023-10-19T15:06:35.165Z', 'cfstEvent': '2023-10-19T07:06:24.156Z', 'sp2stEvent': '2023-10-19T07:06:25.676Z', 'wcstEvent': None}, 'watercare': None, 'online': None, 'pumps': [{'id': 'P2', 'type': 'JET', 'state': 'OFF', 'speed': 'ONE_SPEED', 'current': None}, {'id': 'P1', 'type': 'JET', 'state': 'LOW', 'speed': 'TWO_SPEED', 'current': None}], 'lights': [{'zone': 1, 'mode': 'ON', 'cycleSpeed': 0, 'color': {'red': 0, 'blue': 0, 'green': 0, 'white': 0}, 'intensity': 0, 'irt': None, 'exterior': False}], 'sensors': [], 'lowRangeLowTemp': 65, 'lowRangeHighTemp': 99, 'highRangeLowTemp': 80, 'highRangeHighTemp': 104, 'tempRange': 'HIGH', 'heater1Present': 'PRESENT', 'heater2Present': 'NOT_PRESENT', 'ozoneSystemPresent': 'NOT_PRESENT', 'primingMode': 'INACTIVE', 'heater2On': 'OFF', 'heatPumpStatus': 'NOT_PRESENT', 'heatPumpMode': 'DISABLED', 'heatPumpEfficiency': 'AUTO_SMART', 'electricHeaterMode': 'M7', 'czStatus': 'NOT_PRESENT', 'chromazon3Present': 'OFF', 'chromazon3Zone1': 'FULL_CONTROL', 'chromazon3Zone2': 'FULL_CONTROL', 'chromazon3Zone3': 'FULL_CONTROL', 'heatCanWait': 4, 'heatVacation': False, 'signal': {'strength': 12, 'quality': 6, 'signalAt': None, 'country': 'US', 'updateAt': '2023-10-19T11:45:54.049Z'}, 'errors': [], 'timeSet': None}
2023-10-19 09:05:46.363 ERROR (MainThread) [homeassistant.components.smarttub.controller] Unexpected error fetching smarttub data: None
Traceback (most recent call last):
File "/usr/src/homeassistant/homeassistant/helpers/update_coordinator.py", line 290, in _async_refresh
self.data = await self._async_update_data()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/src/homeassistant/homeassistant/helpers/update_coordinator.py", line 246, in _async_update_data
return await self.update_method()
^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/src/homeassistant/homeassistant/components/smarttub/controller.py", line 89, in async_update_data
data[spa.id] = await self._get_spa_data(spa)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/src/homeassistant/homeassistant/components/smarttub/controller.py", line 96, in _get_spa_data
full_status, reminders, errors = await asyncio.gather(
^^^^^^^^^^^^^^^^^^^^^
File "/usr/local/lib/python3.11/site-packages/smarttub/api.py", line 215, in get_status_full
return SpaStateFull(self, full_status)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/local/lib/python3.11/site-packages/smarttub/api.py", line 352, in __init__
super().__init__(spa, **state)
File "/usr/local/lib/python3.11/site-packages/smarttub/api.py", line 280, in __init__
self._prop("blowoutCycle", constructor=lambda x: self.CycleStatus[x])
File "/usr/local/lib/python3.11/site-packages/smarttub/api.py", line 341, in _prop
self, instance_variable_name, constructor(self.properties[json_key])
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/local/lib/python3.11/site-packages/smarttub/api.py", line 280, in <lambda>
self._prop("blowoutCycle", constructor=lambda x: self.CycleStatus[x])
~~~~~~~~~~~~~~~~^^^
File "/usr/local/lib/python3.11/enum.py", line 790, in __getitem__
return cls._member_map_[name]
~~~~~~~~~~~~~~~~^^^^^^
KeyError: None
2023-10-19 09:05:46.384 DEBUG (MainThread) [homeassistant.components.smarttub.controller] Finished fetching smarttub data in 0.311 seconds (success: False)
2023-10-19 09:05:46.594 ERROR (MainThread) [homeassistant.components.binary_sensor] Error while setting up smarttub platform for binary_sensor
Traceback (most recent call last):
File "/usr/src/homeassistant/homeassistant/helpers/entity_platform.py", line 359, in _async_setup_platform
await asyncio.shield(task)
File "/usr/src/homeassistant/homeassistant/components/smarttub/binary_sensor.py", line 56, in async_setup_entry
for reminder in controller.coordinator.data[spa.id][ATTR_REMINDERS].values()
~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
TypeError: 'NoneType' object is not subscriptable
2023-10-19 09:05:46.604 ERROR (MainThread) [homeassistant.components.light] Error while setting up smarttub platform for light
Traceback (most recent call last):
File "/usr/src/homeassistant/homeassistant/helpers/entity_platform.py", line 359, in _async_setup_platform
await asyncio.shield(task)
File "/usr/src/homeassistant/homeassistant/components/smarttub/light.py", line 36, in async_setup_entry
entities = [
^
File "/usr/src/homeassistant/homeassistant/components/smarttub/light.py", line 39, in <listcomp>
for light in controller.coordinator.data[spa.id][ATTR_LIGHTS].values()
~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
TypeError: 'NoneType' object is not subscriptable
2023-10-19 09:05:46.624 ERROR (MainThread) [homeassistant.components.switch] Error while setting up smarttub platform for switch
Traceback (most recent call last):
File "/usr/src/homeassistant/homeassistant/helpers/entity_platform.py", line 359, in _async_setup_platform
await asyncio.shield(task)
File "/usr/src/homeassistant/homeassistant/components/smarttub/switch.py", line 24, in async_setup_entry
entities = [
^
File "/usr/src/homeassistant/homeassistant/components/smarttub/switch.py", line 27, in <listcomp>
for pump in controller.coordinator.data[spa.id][ATTR_PUMPS].values()
~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
TypeError: 'NoneType' object is not subscriptable`
```


### Additional information

_No response_
